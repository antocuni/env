# nba-schedule.py

Shows NBA games visible in Italy (Sky Sport / Amazon Prime) for the last 2 days
and next 7 days, with LLM-assigned watchability grades for past games and Italian
commentary detection for upcoming Sky games.

Also available as `bin/nba-schedule.py` (symlink).

## Usage

```
nba-schedule.py                  # normal output, grades past games automatically
nba-schedule.py --no-grade       # fast, no network calls beyond the NBA schedule
nba-schedule.py --conky          # compact format for conky widget
nba-schedule.py --days-back N    # show N days in the past (default 2)
nba-schedule.py --days-ahead N   # show N days ahead (default 7)
```

## Requirements

Python packages: `pytz`, `requests`

External programs:
- `lynx` — fetches and converts HTML to plain text (used for Sky Sport articles)
- `llm` — CLI LLM tool (https://llm.datasette.io/), must have a working default model

## Data sources

### Schedule
`https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_19.json`

The NBA publishes a region-specific schedule JSON for each broadcaster region.
Region 19 is Italy. Each game entry includes `intlTvBroadcasters` (Sky Sport) and
`intlOttBroadcasters` (Amazon Prime) fields. Games without either are filtered out.
The schedule uses US dates (`MM/DD/YYYY`); games are grouped by their **Italian date**
(games at e.g. 01:30 CET Tuesday belong to Tuesday, not Monday).

### Grading (past games)
Sky Sport Italy publishes a daily "results of the night" article at URLs like:
`https://sport.sky.it/nba/YYYY/MM/DD/nba-risultati-partite-notte-N-mese-video`

`find_sky_article()` scrapes the Sky Sport NBA index page with `lynx -listonly`
and finds the article matching the target date. The article text is then passed
to `llm` with a system prompt that asks it to grade **only the specific games we
need** (by tricode, e.g. `LAL @ DAL`) on a 1–10 watchability scale, outputting
lines in the exact format `TRI @ TRI: N`. This avoids fuzzy name matching
entirely — the LLM returns tricodes, we match them exactly.

Grades are cached in `~/.cache/nba/grades.json` keyed by NBA game ID:
```json
{
  "0022501142": {"away": "HOU", "home": "GSW", "date": "2026-04-06", "grade": 9}
}
```
A `null` grade means we tried but the Sky article didn't cover it (game not on Sky,
or article not yet published). Null entries are never retried (the article only
covers recent past).

`GRADE_DELAY = 5h` — we wait 5 hours after tip-off before attempting to grade,
to give Sky Sport time to publish the article.

### Commentary detection (upcoming Sky games)
Sky Sport Italy maintains a rolling season article at a fixed URL
(`SKY_SEASON_URL`) that lists the next ~2 upcoming Sky broadcasts with commentary
info ("commento originale" vs named Italian commentators).

`update_commentary()` fetches this article and asks `llm` to label each Sky game
as `italian` or `original`, again using tricodes for exact matching. Result:
```json
{
  "0022501143": {"away": "NYK", "home": "ATL", "commentary": "italian", "checked_at": "..."}
}
```

**Retry logic:** a `null` commentary (article didn't cover the game yet) is retried
after 12 hours. A confirmed label (`italian`/`original`) is never retried.
The article only shows ~2 games ahead, so most future games start as `null` and
get confirmed as they approach.

`SKY_SEASON_URL` is hardcoded for the 2025-26 season and must be updated each year.

## Conky integration

`conky/nba.conky` runs `nba-schedule.py --conky` every hour via `execpi 3600`.
It is positioned above `main.conky` (both `bottom_right`; adjust `gap_y` to taste).
`conky/myconky.py` starts both conky instances.

### Conky output format
```
Mon 06/04 ◀
  01:30  LAL @ DAL  Sky    [7]
  04:00  HOU @ GSW  Sky    [9]
Tue 07/04
  01:00  NYK @ ATL  Sky        █████   ← Italian commentary flag (green/white/red blocks)
```

**Colors:**
- Orange — day headers
- Yellow — games played in the last 24h
- Grey — games played more than 24h ago
- Green — today's game at an Italian-friendly hour (18:00–23:59, watchable live)
- White — future games

**Commentary flags:** rendered as three colored `█` block characters since conky's
Xft renderer cannot compose Unicode regional indicator letters into flag emoji.
- Italian (`#009246` green / white / `#ce2b37` red) — game has Italian commentary
- USA (`#3C3B6E` blue / white / `#B22234` red) — game confirmed original (English) only
- No flag — commentary not yet known (Prime games, or Sky games not yet in the article)

**Column alignment:** the grade `[N]` and the Italian flag occupy the same column.
If a game has no grade but has Italian commentary, 5 spaces are inserted to keep
the flag aligned with the `[N]` of other games.
