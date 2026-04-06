#!/usr/bin/env python3
"""
NBA games visible in Italy (Sky Sport / Amazon Prime).
Default: last 2 days + next 7 days.
"""
import argparse
import sys
from datetime import datetime, date, timedelta
import pytz
import requests

ITALY_TZ = pytz.timezone('Europe/Rome')
ITALY_REGION = 19
CDN_URL = f"https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_{ITALY_REGION}.json"

OTT_FIELDS = {'intlOttBroadcasters'}
TV_FIELDS = {'intlTvBroadcasters'}

def fetch_schedule():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    resp = requests.get(CDN_URL, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()['leagueSchedule']['gameDates']


def get_channels(broadcasters: dict, short: bool = False) -> list[str]:
    channels = []
    for field in TV_FIELDS:
        for b in broadcasters.get(field, []):
            name = b['broadcasterDisplay']
            channels.append('Sky' if short else name)
    for field in OTT_FIELDS:
        for b in broadcasters.get(field, []):
            name = b['broadcasterDisplay']
            if name.lower() == 'prime':
                name = 'Amazon Prime'
            channels.append('Prime' if short else name)
    return channels


def collect_games(game_dates, start: date, end: date) -> dict[date, list]:
    """Returns {day: [game_info, ...]} for games with Italian TV coverage.
    Games are grouped by their Italian date (not the NBA US date)."""
    by_day: dict[date, list] = {}
    for gdate in game_dates:
        # Pre-filter by NBA date with a ±1 day margin to catch cross-midnight games
        nba_d = datetime.strptime(gdate['gameDate'][:10], '%m/%d/%Y').date()
        if not (start - timedelta(days=1) <= nba_d <= end + timedelta(days=1)):
            continue
        for g in gdate['games']:
            channels = get_channels(g.get('broadcasters', {}))
            if not channels:
                continue
            utc_dt = datetime.fromisoformat(g['gameDateTimeUTC'].replace('Z', '+00:00'))
            italy_dt = utc_dt.astimezone(ITALY_TZ)
            d = italy_dt.date()  # use the Italian date for grouping
            if not (start <= d <= end):
                continue
            away = g['awayTeam']['teamCity'] + ' ' + g['awayTeam']['teamName']
            home = g['homeTeam']['teamCity'] + ' ' + g['homeTeam']['teamName']
            away_tri = g['awayTeam']['teamTricode']
            home_tri = g['homeTeam']['teamTricode']
            by_day.setdefault(d, []).append({
                'time': italy_dt,
                'away': away,
                'home': home,
                'away_tri': away_tri,
                'home_tri': home_tri,
                'channels': channels,
            })
    # Sort games within each day by time
    for day in by_day:
        by_day[day].sort(key=lambda g: g['time'])
    return dict(sorted(by_day.items()))


def print_normal(by_day: dict, today: date):
    for day, games in by_day.items():
        label = day.strftime('%A %d/%m/%Y')
        if day == today:
            label += '  ← oggi'
        print(f"── {label} ──")
        for g in games:
            channels_str = ' / '.join(g['channels'])
            print(f"  {g['time'].strftime('%H:%M')}  {g['away']} @ {g['home']}")
            print(f"          {channels_str}")
        print()


def game_color(g: dict, now: datetime) -> str:
    """
    Red   = already played
    Green = today, Italian-friendly hour (18:00–23:59) — watchable live in the evening
    White = future
    """
    if now - timedelta(hours=24) <= g['time'] < now:
        return 'yellow'
    if g['time'] < now:
        return 'grey'
    if g['time'].date() == now.date() and 18 <= g['time'].hour <= 23:
        return 'green'
    return 'white'


def print_conky(by_day: dict, today: date):
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
            print(f"${{color {color}}}  {g['time'].strftime('%H:%M')}  {matchup:<8}  {short_channels}")
        if day != list(by_day)[-1]:
            print()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--days-back', type=int, default=2,
                        help='Days in the past to show (default: 2)')
    parser.add_argument('--days-ahead', type=int, default=7,
                        help='Days in the future to show (default: 7)')
    parser.add_argument('--conky', action='store_true',
                        help='Output in compact conky format')
    args = parser.parse_args()

    today = date.today()
    start = today - timedelta(days=args.days_back)
    end = today + timedelta(days=args.days_ahead)

    try:
        game_dates = fetch_schedule()
    except Exception as e:
        print(f"Error fetching schedule: {e}", file=sys.stderr)
        sys.exit(1)

    by_day = collect_games(game_dates, start, end)

    if args.conky:
        print_conky(by_day, today)
    else:
        print(f"NBA in Italia — {start.strftime('%d/%m')} → {end.strftime('%d/%m/%Y')}")
        print()
        if not by_day:
            print("Nessuna partita trovata nel periodo.")
            return
        print_normal(by_day, today)


if __name__ == '__main__':
    main()
