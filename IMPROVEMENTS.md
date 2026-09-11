# Project Volusia — Current State & Improvements

## Status (2026-09-09)
- Backend FastAPI on :8000 (health 200, 48 indicators)
- 48 endpoints live via /data/ prefix
- Gamification: 30 missions, 4 tiers (Explorer, Contributor, Steward, Architect)
- All 17 routes mapped, 8 nav links + category pages + news
- News endpoints return empty arrays (no articles loaded)

## Fixes Applied
1. `/gamification` root endpoint added — returns JSON hub with available endpoints (was 307 redirect)
2. `/api/gamification/stats/{user_id}` — now queries gamification DB instead of hardcoded values
3. `/api/gamification/missions/{user_id}` — returns full mission list with status from contributor file
4. Broken external link `volusia.org/public-safety` → `volusia.org` (was 404)
5. Footer dead links `zqm-labs.github.io/ZQM-Labs/` and `zqm-computing.github.io/ZQM-Computing/` → `github.com/ZQM-Computing`
6. Pre-existing TS errors fixed (Skeleton, EmptyState, ErrorState components added)
7. Stale uvicorn restart fixed 404s on /data/public-safety and /data/government-finance

## Data Coverage
- Populated: Economic (13), Demographics (8), Climate (3), Tourism (3), Housing (3), Education (4), Environment (2), Public Safety (2), Transportation (3), Government Finance (2), Health (5) = 48 total
- Empty (need data): Government Finance = 1 category

## Known Issues
- 7 empty categories need data population
- HTTPS/TLS not yet configured
- 11 untracked files in repo root (cleanup needed)
- volusia.db modified, not committed
- JS asset stale hash issue (resynced, verify after next build)

## Endpoints Working
- /health, /latest, /cvb_hotels, /tourism.json, /api/news.json, /data/indicators.csv
- /data/{economic,demographics,climate,tourism,housing,education,environment,public-safety,transportation,government-finance,health}.json
- /gamification, /gamification/missions/{id}, /gamification/badges/{id}
- /api/gamification/* (stats, missions, pulse, state, visit)
- /api/contribute, /api/contributor, /api/webhook, /api/fetch-status