#!/usr/bin/python3
"""
NBA games visible in Italy (Sky Sport / Amazon Prime).
Default: last 2 days + next 7 days.
Past games are automatically graded via Sky Sport Italy + LLM (cached).
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, date, timedelta
from pathlib import Path

import pytz
import requests

ITALY_TZ = pytz.timezone('Europe/Rome')
ITALY_REGION = 19
CDN_URL = f"https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_{ITALY_REGION}.json"
CACHE_FILE = Path.home() / '.cache' / 'nba' / 'grades.json'
COMMENTARY_CACHE_FILE = Path.home() / '.cache' / 'nba' / 'commentary.json'
SKY_ARTICLE_LOG = Path.home() / '.cache' / 'nba' / 'sky_article.log'
SKY_ARTICLE_LOG_MAX_BYTES = 500_000
SKY_ARTICLE_LOG_BACKUPS = 3
SKY_SEASON_URL = "https://sport.sky.it/nba/2025/10/09/nba-2025-2026-partite-tv-streaming-sky-now"
# Wait this long after game tip-off before trying to grade (article won't exist yet)
GRADE_DELAY = timedelta(hours=3)

OTT_FIELDS = {'intlOttBroadcasters'}
TV_FIELDS = {'intlTvBroadcasters'}


# ── schedule ──────────────────────────────────────────────────────────────────

def fetch_schedule():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    resp = requests.get(CDN_URL, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()['leagueSchedule']['gameDates']


def get_channels(broadcasters: dict) -> list[str]:
    channels = []
    for field in TV_FIELDS:
        for b in broadcasters.get(field, []):
            channels.append(b['broadcasterDisplay'])
    for field in OTT_FIELDS:
        for b in broadcasters.get(field, []):
            name = b['broadcasterDisplay']
            if name.lower() == 'prime':
                name = 'Amazon Prime'
            channels.append(name)
    return channels


def collect_games(game_dates, start: date, end: date) -> dict[date, list]:
    """Returns {italian_day: [game_info, ...]} for games with Italian TV coverage."""
    by_day: dict[date, list] = {}
    for gdate in game_dates:
        nba_d = datetime.strptime(gdate['gameDate'][:10], '%m/%d/%Y').date()
        if not (start - timedelta(days=1) <= nba_d <= end + timedelta(days=1)):
            continue
        for g in gdate['games']:
            channels = get_channels(g.get('broadcasters', {}))
            if not channels:
                continue
            utc_dt = datetime.fromisoformat(g['gameDateTimeUTC'].replace('Z', '+00:00'))
            italy_dt = utc_dt.astimezone(ITALY_TZ)
            d = italy_dt.date()
            if not (start <= d <= end):
                continue
            by_day.setdefault(d, []).append({
                'game_id': g['gameId'],
                'time': italy_dt,
                'away': g['awayTeam']['teamCity'] + ' ' + g['awayTeam']['teamName'],
                'home': g['homeTeam']['teamCity'] + ' ' + g['homeTeam']['teamName'],
                'away_tri': g['awayTeam']['teamTricode'],
                'home_tri': g['homeTeam']['teamTricode'],
                'channels': channels,
            })
    for day in by_day:
        by_day[day].sort(key=lambda g: g['time'])
    return dict(sorted(by_day.items()))


# ── grading ───────────────────────────────────────────────────────────────────

def load_grades() -> dict:
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text())
    return {}


def save_grades(grades: dict):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(grades, indent=2, sort_keys=True))


def find_sky_article(target_date: date) -> str | None:
    """Find the Sky Sport Italy NBA results article URL for a given date."""
    try:
        result = subprocess.run(
            ['lynx', '-dump', '-listonly', 'https://sport.sky.it/nba'],
            capture_output=True, text=True, timeout=15,
        )
    except Exception:
        return None
    candidate_dates = {target_date.strftime('%Y/%m/%d'),
                       (target_date - timedelta(days=1)).strftime('%Y/%m/%d')}
    for line in result.stdout.splitlines():
        parts = line.split()
        url = parts[-1] if parts else ''
        if re.search(r'nba.*(partite|risultati).*notte', url) and any(d in url for d in candidate_dates):
            return url
    return None


def fetch_sky_text(url: str) -> str:
    result = subprocess.run(
        ['lynx', '-dump', '-nolist', url],
        capture_output=True, text=True, timeout=30,
    )
    return result.stdout


def grade_via_llm(article_text: str, games: list) -> dict[str, int]:
    """
    Ask the LLM to grade specific games using the article as context.
    Returns {game_id: grade}. Output format enforced as 'TRI @ TRI: N'.
    """
    game_list = ', '.join(f"{g['away_tri']} @ {g['home_tri']}" for g in games)
    system_prompt = (
        "You will receive a summary of NBA games. "
        "Grade each of the following games for watchability on a scale of 1 (boring blowout) "
        "to 10 (thrilling finish decided in the last seconds or OT). "
        "Do NOT reveal scores or results. "
        f"Grade ONLY these games: {game_list}. "
        "Output ONLY lines in the exact format: 'TRI1 @ TRI2: N'  (e.g. 'LAL @ DAL: 7'). "
        "Nothing else."
    )
    result = subprocess.run(
        ['llm', '-s', system_prompt],
        input=article_text, capture_output=True, text=True, timeout=60,
    )
    grades = {}
    for line in result.stdout.splitlines():
        m = re.match(r'^([A-Z]+)\s*@\s*([A-Z]+)\s*:\s*(\d+)', line.strip())
        if m:
            away_tri, home_tri, grade = m.group(1), m.group(2), int(m.group(3))
            for g in games:
                if g['away_tri'] == away_tri and g['home_tri'] == home_tri:
                    grades[g['game_id']] = grade
                    break
    return grades


def _needs_grade(game_id: str, grades: dict, now: datetime) -> bool:
    entry = grades.get(game_id)
    if entry is None:
        return True
    if entry['grade'] is not None:
        return False  # already graded
    # Null grade: retry for up to 24h after the first attempt, then give up
    checked_at_str = entry.get('checked_at')
    if not checked_at_str:
        return True  # old null entry without timestamp — retry once
    checked_at = datetime.fromisoformat(checked_at_str)
    return (now - checked_at) < timedelta(hours=24)


def grade_past_games(by_day: dict, grades: dict, now: datetime) -> bool:
    """Grade ungraded past games by day. Writes cache if anything changed."""
    updated = False
    for day, games in by_day.items():
        ungraded = [
            g for g in games
            if _needs_grade(g['game_id'], grades, now) and g['time'] + GRADE_DELAY < now
        ]
        if not ungraded:
            continue

        url = find_sky_article(day)
        if not url:
            for game in ungraded:
                grades[game['game_id']] = {
                    'date': day.isoformat(),
                    'away': game['away_tri'],
                    'home': game['home_tri'],
                    'grade': None,
                    'checked_at': now.isoformat(),
                }
            updated = True
            continue

        text = fetch_sky_text(url)
        llm_grades = grade_via_llm(text, ungraded)

        for game in ungraded:
            grades[game['game_id']] = {
                'date': day.isoformat(),
                'away': game['away_tri'],
                'home': game['home_tri'],
                'grade': llm_grades.get(game['game_id']),
                'checked_at': now.isoformat(),
            }
        updated = True

    if updated:
        save_grades(grades)
    return updated


# ── commentary ────────────────────────────────────────────────────────────────

def load_commentary() -> dict:
    if COMMENTARY_CACHE_FILE.exists():
        return json.loads(COMMENTARY_CACHE_FILE.read_text())
    return {}


def save_commentary(commentary: dict):
    COMMENTARY_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    COMMENTARY_CACHE_FILE.write_text(json.dumps(commentary, indent=2, sort_keys=True))


def fetch_sky_season_article() -> str:
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    resp = requests.get(SKY_SEASON_URL, headers=headers, timeout=15)
    resp.raise_for_status()
    # Use lynx to get clean text from the HTML
    result = subprocess.run(
        ['lynx', '-dump', '-nolist', '-stdin'],
        input=resp.text, capture_output=True, text=True, timeout=15,
    )
    text = result.stdout
    _log_sky_article(text)
    return text


def _log_sky_article(text: str):
    SKY_ARTICLE_LOG.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(text.encode()).hexdigest()
    hash_file = SKY_ARTICLE_LOG.with_suffix('.log.hash')
    if hash_file.exists() and hash_file.read_text().strip() == digest:
        return  # content unchanged, skip
    _rotate_log(SKY_ARTICLE_LOG, SKY_ARTICLE_LOG_MAX_BYTES, SKY_ARTICLE_LOG_BACKUPS)
    with SKY_ARTICLE_LOG.open('a') as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Fetched at: {datetime.now(tz=ITALY_TZ).isoformat()}\n")
        f.write(f"URL: {SKY_SEASON_URL}\n")
        f.write('='*60 + '\n')
        f.write(text)
    hash_file.write_text(digest)


def _rotate_log(path: Path, max_bytes: int, backups: int):
    if not path.exists() or path.stat().st_size < max_bytes:
        return
    for i in range(backups - 1, 0, -1):
        src = Path(f"{path}.{i}")
        dst = Path(f"{path}.{i + 1}")
        if src.exists():
            src.rename(dst)
    path.rename(Path(f"{path}.1"))


def detect_commentary_via_llm(article_text: str, games: list) -> dict[str, str]:
    """
    Ask LLM to label each game as 'italian' or 'original' based on the Sky article.
    Returns {game_id: 'italian' | 'original'}.
    """
    game_list = ', '.join(
        f"{g['away_tri']} @ {g['home_tri']} on {g['time'].strftime('%Y-%m-%d')}"
        for g in games
    )
    system_prompt = (
        "You will receive a Sky Sport Italy NBA broadcast schedule. "
        "For each game, determine if Italian commentary is available — "
        "either for the live broadcast or for any replay of that game. "
        "If named Italian commentators appear anywhere for that game (live or replay), label it 'italian'. "
        "The article may not mention the live broadcast time; in that case use the replay date "
        "to identify which game in a series it refers to (e.g. a replay on April 20 belongs to the game "
        "played on the night of April 19-20). "
        "The article may list multiple games between the same two teams (playoff series): "
        "match each request to the correct game by date. "
        "If the live game is marked '***UNICO PASSAGGIO***' with only 'commento originale' and no named "
        "Italian commentators anywhere for that game entry, label it 'original'. "
        f"Label ONLY these games: {game_list}. "
        "Output ONLY lines in the exact format: 'TRI1 @ TRI2 on YYYY-MM-DD: italian' or 'TRI1 @ TRI2 on YYYY-MM-DD: original'. "
        "Nothing else."
    )
    result = subprocess.run(
        ['llm', '-s', system_prompt],
        input=article_text, capture_output=True, text=True, timeout=30,
    )
    detected = {}
    for line in result.stdout.splitlines():
        m = re.match(
            r'^([A-Z]+)\s*@\s*([A-Z]+)\s+on\s+(\d{4}-\d{2}-\d{2})\s*:\s*(italian|original)',
            line.strip(), re.IGNORECASE,
        )
        if m:
            away_tri, home_tri, date_str, label = m.group(1), m.group(2), m.group(3), m.group(4).lower()
            for g in games:
                if (g['away_tri'] == away_tri and g['home_tri'] == home_tri
                        and g['time'].strftime('%Y-%m-%d') == date_str):
                    detected[g['game_id']] = label
                    break
    return detected


def _needs_commentary_check(game_id: str, commentary: dict, now: datetime) -> bool:
    entry = commentary.get(game_id)
    if entry is None:
        return True  # never tried
    if entry['commentary'] is not None:
        return False  # already confirmed
    # Not found last time — retry after 12 hours
    checked_at_str = entry.get('checked_at')
    if not checked_at_str:
        return True
    checked_at = datetime.fromisoformat(checked_at_str).replace(tzinfo=ITALY_TZ)
    return (now - checked_at) > timedelta(hours=12)


def update_commentary(by_day: dict, commentary: dict) -> bool:
    """Fetch Sky season article and update commentary cache for Sky games not yet labelled."""
    now = datetime.now(tz=ITALY_TZ)
    sky_games = [
        g for games in by_day.values() for g in games
        if any('sky' in ch.lower() for ch in g['channels'])
        and _needs_commentary_check(g['game_id'], commentary, now)
    ]
    if not sky_games:
        return False

    try:
        text = fetch_sky_season_article()
    except Exception:
        return False

    detected = detect_commentary_via_llm(text, sky_games)
    checked_at = now.isoformat()

    for game in sky_games:
        game_id = game['game_id']
        commentary[game_id] = {
            'away': game['away_tri'],
            'home': game['home_tri'],
            'commentary': detected.get(game_id),  # None if article doesn't cover it yet
            'checked_at': checked_at,
        }
    save_commentary(commentary)
    return True


# ── display ───────────────────────────────────────────────────────────────────

def game_color(g: dict, now: datetime) -> str:
    """
    Yellow = played in the last 24h
    Grey   = played earlier
    Green  = today, Italian-friendly hour (18:00–23:59)
    White  = future
    """
    if now - timedelta(hours=24) <= g['time'] < now:
        return 'yellow'
    if g['time'] < now:
        return 'grey'
    if g['time'].date() == now.date() and 18 <= g['time'].hour <= 23:
        return 'green'
    return 'white'


def fmt_grade(game_id: str, grades: dict) -> str:
    entry = grades.get(game_id)
    if entry is None or entry['grade'] is None:
        return ''
    return f"  [{entry['grade']}]"


def commentary_flag(game_id: str, commentary: dict, conky: bool = False) -> str:
    entry = commentary.get(game_id)
    if not entry:
        return ''
    if entry['commentary'] == 'italian':
        if conky:
            return ' ${color #009246}█${color white}█${color #ce2b37}█${color white}'
        return ' 🇮🇹'
    if entry['commentary'] == 'original':
        if conky:
            return ' ${font Noto Color Emoji}🌎${font}'
        return ' 🌎'
    return ''


def print_normal(by_day: dict, today: date, grades: dict, commentary: dict):
    for day, games in by_day.items():
        label = day.strftime('%A %d/%m/%Y')
        if day == today:
            label += '  ← oggi'
        print(f"── {label} ──")
        for g in games:
            channels_str = ' / '.join(g['channels'])
            grade_str = fmt_grade(g['game_id'], grades)
            ita = commentary_flag(g['game_id'], commentary)
            print(f"  {g['time'].strftime('%H:%M')}  {g['away']} @ {g['home']}{grade_str}{ita}")
            print(f"          {channels_str}")
        print()


def print_conky(by_day: dict, today: date, grades: dict, commentary: dict):
    now = datetime.now(tz=ITALY_TZ)
    for day, games in by_day.items():
        label = day.strftime('%a %d/%m')
        if day == today:
            label += ' ◀'
        print(f'${{color orange}}{label}')
        for g in games:
            short_channels = ' / '.join(
                'Sky' if 'sky' in ch.lower() else 'Prime'
                for ch in g['channels']
            )
            matchup = f"{g['away_tri']} @ {g['home_tri']}"
            color = game_color(g, now)
            entry = grades.get(g['game_id'])
            has_grade = entry and entry['grade'] is not None
            is_ita = commentary.get(g['game_id'], {}).get('commentary') in ('italian', 'original')
            # Grade slot is always 5 chars wide ("  [N]"); pad with spaces if no grade
            if has_grade:
                grade_part = f"  [{entry['grade']}]"
            elif is_ita:
                grade_part = "     "   # same width as "  [N]"
            else:
                grade_part = ""
            ita_part = commentary_flag(g['game_id'], commentary, conky=True) if is_ita else ''
            print(f"${{color {color}}}  {g['time'].strftime('%H:%M')}  {matchup:<9} {short_channels:<5}{grade_part}{ita_part}")
        if day != list(by_day)[-1]:
            print()


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--days-back', type=int, default=2,
                        help='Days in the past to show (default: 2)')
    parser.add_argument('--days-ahead', type=int, default=2,
                        help='Days in the future to show (default: 2)')
    parser.add_argument('--no-grade', action='store_true',
                        help='Skip grading (faster, no network calls to Sky/LLM)')
    parser.add_argument('--conky', action='store_true',
                        help='Output in compact conky format')
    parser.add_argument('--clear-cache', action='store_true',
                        help='Delete grades and commentary caches, then exit')
    parser.add_argument('--show-grade-article', metavar='DATE', nargs='?',
                        const=date.today().isoformat(),
                        help='Fetch and print the Sky grading article for DATE (YYYY-MM-DD, default: today), then exit')
    args = parser.parse_args()

    if args.show_grade_article is not None:
        try:
            target = date.fromisoformat(args.show_grade_article)
        except ValueError:
            print(f"Invalid date: {args.show_grade_article!r}. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
        url = find_sky_article(target)
        if not url:
            print(f"No Sky grading article found for {target}.", file=sys.stderr)
            sys.exit(1)
        print(f"Article URL: {url}\n", file=sys.stderr)
        print(fetch_sky_text(url))
        return

    if args.clear_cache:
        for f in (CACHE_FILE, COMMENTARY_CACHE_FILE):
            if f.exists():
                f.unlink()
                print(f"Deleted {f}")
            else:
                print(f"Not found: {f}")
        return

    today = date.today()
    start = today - timedelta(days=args.days_back)
    end = today + timedelta(days=args.days_ahead)

    try:
        game_dates = fetch_schedule()
    except Exception as e:
        print(f"Error fetching schedule: {e}", file=sys.stderr)
        sys.exit(1)

    by_day = collect_games(game_dates, start, end)
    grades = load_grades()
    commentary = load_commentary()

    if not args.no_grade:
        now = datetime.now(tz=ITALY_TZ)
        grade_past_games(by_day, grades, now)
        update_commentary(by_day, commentary)

    if args.conky:
        print_conky(by_day, today, grades, commentary)
    else:
        print(f"NBA in Italia — {start.strftime('%d/%m')} → {end.strftime('%d/%m/%Y')}")
        print()
        if not by_day:
            print("Nessuna partita trovata nel periodo.")
            return
        print_normal(by_day, today, grades, commentary)
        print()
        print(SKY_SEASON_URL)

if __name__ == '__main__':
    main()
