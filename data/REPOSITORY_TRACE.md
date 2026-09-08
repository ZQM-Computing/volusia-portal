# Project Volusia — Full Repository Trace

> **Date**: 2026-09-08
> **Repo**: [ZQM-Computing/volusia-portal](https://github.com/ZQM-Computing/volusia-portal)
> **Host**: ZQM-NODE-4 / 192.168.1.217 (Windows 10)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        BROWSER (React SPA)                              │
│  src/App.tsx → Routes → src/pages/*.tsx                                │
│  src/hooks/useApi.ts → fetch('/data/*')                                │
│  src/components/Layout.tsx → Header/Footer + gamification stats          │
└──────────────────────────┬────────────────────────────────────────────┘
                           │ HTTP GET /data/*.json (proxied through nginx)
                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     NGINX :80 (Windows Service)                         │
│  conf.d/default.conf                                                     │
│  location /data/*.json → proxy_pass http://127.0.0.1:8000/data/*.json  │
│  location /indicators → proxy_pass http://127.0.0.1:8000/indicators    │
│  location /api/ → proxy_pass http://127.0.0.1:8000/                      │
│  location /gamification → proxy_pass http://127.0.0.1:8000/gamification │
│  location /health → proxy_pass http://127.0.0.1:8000/health            │
│  All other → serves static files from dist/                             │
└──────────────────────────┬────────────────────────────────────────────┘
                           │ proxy_pass
                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              FASTAPI BACKEND :8000 (uvicorn, native Python)             │
│  backend/main.py                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Routes:                                                         │   │
│  │  GET /                          → root info                       │   │
│  │  GET /health                    → DB health check                 │   │
│  │  GET /indicators                → all indicators from DB          │   │
│  │  GET /indicators/{name}         → single indicator by name       │   │
│  │  GET /indicators/category/{cat} → filtered by category           │   │
│  │  GET /indicators.csv            → CSV download                     │   │
│  │  GET /datasets                  → dataset catalog from DB         │   │
│  │  GET /map-layers                → map layers from DB              │   │
│  │  GET /data/indicators.json      → indicators as JSON              │   │
│  │  GET /data/{name}.json          → cached JSON file from cache/    │   │
│  │  GET /pulse.json                → gamification pulse              │   │
│  │  GET /refresh                   → diagnostics (no auth!)          │   │
│  │  GET /diagnostics               → full system diagnostics         │   │
│  │  POST /refresh                  → trigger refresh pipeline        │   │
│  │              (requires HMAC secret via ?secret=)                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Gamification (backend/gamification.py):                         │   │
│  │  GET /gamification/stats/{userId}                               │   │
│  │  GET /gamification/leaderboard                                  │   │
│  │  POST /gamification/visit/{userId}                              │   │
│  │  GET /gamification/missions                                     │   │
│  │  POST /gamification/contribute                                  │   │
│  │  └── Scoring: backend/gamification/scoring.py (APIRouter)      │   │
│  │      BUT NOT imported by main.py! (known bug)                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ DB: backend/data/volusia.db (SQLite 80KB)                       │   │
│  │  Tables: indicators(26), map_layers(18), datasets(10),           │   │
│  │          gamification(2 users), gamification_history,           │   │
│  │          cvb_hotels(0 rows!), audit_log                         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└──────────────────────────┬────────────────────────────────────────────┘
                           │ reads from
                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    DATA CACHE (data/cache/*.json)                       │
│  29 JSON files, served by GET /data/{name}.json                         │
│                                                                          │
│  ACTIVE CACHE (served by backend):                                       │
│  ├── indicators.json (29 indicators across 4 categories)               │
│  ├── economic.json (6 indicators: income, unemployment, poverty,        │
│  │   cost_of_living, col_overall, per_capita_income_acs=-888888888)     │
│  ├── demographics.json (8 indicators: population, age, bachelors,       │
│  │   white_alone=579622.0[BUG], pct_over_65=25.4)                       │
│  ├── climate.json (5 indicators: avg_max_temp, avg_min_temp,            │
│  │   total_precip, plus dated 2024 variants)                            │
│  ├── tourism.json (3 indicators: hotel_occupancy, avg_daily_rate,      │
│  │   revpar — all vintage "December 2021")                              │
│  ├── map-layers.json (18 layers with GeoJSON geometry)                 │
│  ├── datasets.json (10 datasets, ALL content="")                        │
│  └── news.json (1 article, 18 bytes)                                    │
│                                                                          │
│  STALE/EMPTY CACHE (NOT served by /data/{name}.json route):            │
│  ├── business.json, education.json, safety.json, government.json,      │
│  │   housing.json, transportation.json, environment.json — all          │
│  │   contain {"count":0,"indicators":[],"message":"..."}               │
│  ├── bea_income.json, census_dp03.json, census_dp05.json —            │
│  │   raw API response format (different structure!)                     │
│  ├── noaa_daily.json, noaa_daily_2025-09-*.json, open_meteo_forecast,  │
│  │   redfin.json, redfin_volusia.json, zillow_zhvi.json —              │
│  │   raw API response format (different structure!)                     │
│  └── volusia_business.json, volusia_gis.json, stakeholders.json —      │
│      different structure entirely                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## File-by-File Trace

### Frontend (React + Vite + TypeScript + Tailwind)

```
src/
├── App.tsx                    # React Router config — 9 routes → 9 page components
│                              # Routes: /, /data, /maps, /business, /residents,
│                              #           /tourists, /leaders, /gamification, /news
│
├── components/
│   ├── Layout.tsx             # Header (nav links + dark mode toggle) + Footer
│   │                          # Uses useGamificationStats('anonymous') + useDiagnostics()
│   │                          # Nav: Portal Home, Data Explorer, Maps, Business,
│   │                          #      Residents, Tourists, Leaders, Gamification
│   └── UI.tsx                 # Shared UI components: Card, SectionTitle, Badge,
│                              #   DataSource, StatCard (value/label/change/changeLabel)
│
├── hooks/
│   └── useApi.ts              # SINGLE HOOK FILE — all API calls go here
│                              # API_BASE = '/data' (proxied through nginx)
│                              #
│                              # Generic: useApiData<T>(endpoint) → {data, loading, error}
│                              #
│                              # Category hooks (fetch /data/{name}.json):
│                              #   useAllIndicators()      → /indicators.json
│                              #   useEconomicIndicators() → /economic.json
│                              #   useDemographicIndicators() → /demographics.json
│                              #   useClimateIndicators()  → /climate.json
│                              #   useDatasets()           → /datasets.json
│                              #   useMapLayers()          → /map-layers.json
│                              #   useNews()               → /news.json (404!)
│                              #   useHealth()             → /health.json
│                              #   useStakeholderGroups()  → /stakeholders.json
│                              #
│                              # Download: useDownloadCSV(category?) → window.open()
│                              #
│                              # Single item: useIndicator(name) → /indicators/{name}
│                              # List:      useIndicatorList() → /indicators.json
│                              #
│                              # Gamification hooks:
│                              #   useGamification(userId) → visitPage + pulse
│                              #   useGamificationStats(userId) → stats/XP/level
│                              #   useLeaderboard() → /gamification/leaderboard
│                              #   useDiagnostics() → /diagnostics
│
├── pages/
│   ├── HomePage.tsx           # Portal home — 4 StatCards + 2 charts + climate section
│   │                          # Uses: useEconomicIndicators, useDemographicIndicators,
│   │                          #       useClimateIndicators, useMapLayers, useDatasets
│   │                          # Charts: IncomeTrendData, EmploymentTrendData
│   │                          # Climate: avg_max_temp, total_precip, avg_min_temp
│   │
│   ├── DataExplorerPage.tsx   # Data catalog + charts + filters + download buttons
│   │                          # Uses: useDatasets, useIndicatorList, useMapLayers,
│   │                          #       useDownloadCSV
│   │                          # Charts: Unemployment (ResponsiveLine), Income (ResponsiveBar)
│   │                          # Filter: categoryFilter via d.source (BUG: should be d.category)
│   │                          # Download CSV: window.open('/data/indicators.csv') (404!)
│   │
│   ├── ResidentsPage.tsx      # Resident data — 5 StatCards + income trend + cost of living
│   │                          # Uses: useDemographicIndicators, useEconomicIndicators,
│   │                          #       useClimateIndicators
│   │                          # StatCards: Median Household Income, Population, Median Age,
│   │                          #           Population 65+, Bachelor's+
│   │                          # Empty sections: Education, Safety, Environment,
│   │                          #               Housing, Transportation, Government
│   │
│   ├── BusinessPage.tsx       # Business dashboard — employment, industry mix, cost of living
│   │                          # Uses: useEconomicIndicators, useDemographicIndicators,
│   │                          #       useClimateIndicators, useDownloadCSV
│   │                          # Charts: QCEW employment trend, industry mix bar chart
│   │                          # Hardcoded: businessFormation array, industryMix array
│   │                          # Dead-end: 3 "Coming Soon" resource cards
│   │
│   ├── TouristsPage.tsx       # Tourist intelligence — hotel occupancy, visitor volume
│   │                          # Uses: useEconomicIndicators, useDemographicIndicators,
│   │                          #       useClimateIndicators
│   │                          # Conditions: hotelOccupancy, avgDailyRate, revpar, Population
│   │                          # Chart: Monthly Visitor Volume (hardcoded 12 months)
│   │                          # Dead-end: 3 resource cards (Event Calendar, Reviews, Parking)
│   │
│   ├── LeadersPage.tsx        # Leaders intelligence — investment, workforce, permitting
│   │                          # Uses: useLeaderboard, useEconomicIndicators
│   │                          # Charts: Capital Investment (ResponsiveBar), Workforce (ResponsivePie)
│   │                          # Stats: Total Employment, Population, Personal Income, Leaderboard count
│   │                          # PermittingVelocity: hardcoded avgDays (18, 45, 7, 62)
│   │                          # Leaderboard section: renders leaderboardData from useLeaderboard()
│   │
│   ├── MapsPage.tsx           # Interactive maps — GeoJSON layers + city markers
│   │                          # Uses: useMapLayers
│   │                          # Renders: GeoJSON from map layers, category filter
│   │                          # City markers: hardcoded (Daytona Beach, DeLand, etc.)
│   │                          # Toggles: showBoundary (GeoJSON), showCities (Point features)
│   │
│   ├── GamificationPage.tsx   # Gamification hub — XP progress, leaderboard, pulse
│   │                          # Uses: useLeaderboard, useGamification
│   │                          # Displays: XP progress bar, level, leaderboard table, pulse data
│   │                          # Bug: Pulse data all stale (stale_hours: 48)
│   │                          # Bug: Missions never called from frontend
│   │
│   ├── NewsPage.tsx           # News feed — single article
│   │                          # Uses: useNews → /news.json (RETURNS 404!)
│   │                          # Result: Empty page or error
│   │
│   ├── NotFoundPage.tsx       # 404 page — simple link back to home
│   │
│   └── index.tsx              # Entry point — renders <App />
│
├── utils/
│   ├── index.tsx              # ErrorBoundary component
│   └── useDebounce.ts         # useDebounce hook for search input
│
├── types/
│   └── index.ts               # TypeScript type definitions
│
├── assets/                    # Static assets (images, fonts)
├── index.css                  # Tailwind CSS + custom styles
├── main.tsx                   # Entry point — ReactDOM.createRoot
├── vite-env.d.ts              # Vite type declarations
└── App.css                    # (if exists)
```

### Backend (FastAPI + SQLite)

```
backend/
├── main.py                    # FastAPI app — ALL routes defined here
│                              # Key functions:
│                              #   _require_refresh_auth(secret) — HMAC validation
│                              #   _db_rows(query, params) — SQLite query helper
│                              #   _init_gamification_db(conn) — Creates gamification tables
│                              #
│                              # Routes:
│                              #   GET  /                          → root info
│                              #   GET  /health                    → DB health
│                              #   GET  /indicators                → all indicators
│                              #   GET  /indicators/{name}         → single indicator
│                              #   GET  /indicators/category/{cat} → filtered
│                              #   GET  /indicators.csv            → CSV download
│                              #   GET  /datasets                  → dataset catalog
│                              #   GET  /map-layers                → map layers
│                              #   GET  /data/indicators.json      → indicators JSON
│                              #   GET  /data/{name}.json          → cached JSON file
│                              #   GET  /pulse.json                → gamification pulse
│                              #   GET  /refresh                   → diagnostics (NO AUTH!)
│                              #   GET  /diagnostics               → full diagnostics
│                              #   POST /refresh                   → trigger refresh (HMAC auth)
│                              #
│                              # KNOWN BUGS:
│                              #   - /refresh GET has no auth but /refresh POST does
│                              #   - gamification/scoring.py NOT imported (APIRouter not registered)
│                              #   - REFRESH_TOKEN defaults to 'volusia-refresh-secret-change-me'
│                              #   - CORS allows all origins (*)
│
├── gamification.py            # Gamification module
│                              # Functions: get_gamification_routes(app), _init_gamification_db(conn)
│                              # Creates gamification table, registers inline routes
│                              # Routes: /gamification/stats/{id}, /gamification/leaderboard,
│                              #         /gamification/visit/{id}
│                              # KNOWN BUG: Does NOT import scoring.py routes!
│
├── gamification/
│   ├── __init__.py            # Empty (makes it a package)
│   ├── scoring.py             # APIRouter with 8 routes (prefix="/gamification")
│   │                          # Routes: /contribute, /quality, /reputation/{id},
│   │                          #         /leaderboard, /missions, /resync, /pulse, /profile/{id}
│   │                          # KNOWN BUG: NOT imported by main.py! All routes return 404
│   │
│   └── routes.py              # Alternative gamification routes module
│
├── requirements.txt           # Python dependencies (fastapi, uvicorn, sqlalchemy, etc.)
└── Dockerfile.backend         # Docker build config (NOT used — runs natively)
```

### Data Layer

```
data/
├── volusia.db                 # SQLite database (80KB, 7 tables)
│                              # Tables: indicators(26), map_layers(18), datasets(10),
│                          #          gamification(2 users), gamification_history,
│                          #          cvb_hotels(0 rows!), audit_log
│
├── cache/                     # 29 JSON cache files served by GET /data/{name}.json
│   ├── indicators.json        # 29 indicators across 4 categories (PRIMARY)
│   ├── economic.json          # 6 economic indicators (includes per_capita_income_acs=-888888888)
│   ├── demographics.json      # 8 demographic indicators (pct_white_alone=579622.0 BUG)
│   ├── climate.json           # 5 climate indicators (avg_max_temp, avg_min_temp, total_precip)
│   ├── tourism.json           # 3 tourism indicators (all vintage "December 2021")
│   ├── map-layers.json        # 18 layers with GeoJSON geometry
│   ├── datasets.json          # 10 datasets (ALL content="")
│   ├── news.json              # 1 article (18 bytes) — barely any content
│   ├── stakeholders.json      # Stakeholder data
│   │
│   ├── health.json            # Health check data
│   ├── datasets.json          # Duplicate of cache/datasets.json
│   │
│   ├── bea_income.json        # BEA raw API response (different structure!)
│   ├── census_dp03.json       # Census ACS DP03 raw response
│   ├── census_dp05.json       # Census ACS DP05 raw response
│   ├── noaa_daily.json        # NOAA daily summaries raw response
│   ├── noaa_daily_2025-09-02_2026-09-02.json  # Date-range NOAA data
│   ├── noaa_daily_2025-09-03_2026-09-03.json  # Date-range NOAA data
│   ├── open_meteo_forecast.json  # Open-Meteo raw forecast
│   ├── redfin.json            # Redfin raw data
│   ├── redfin_volusia.json    # Redfin Volusia-specific raw data
│   ├── zillow_zhvi.json       # Zillow ZHVI raw data
│   │
│   ├── business.json          # {"count":0,"indicators":[],"message":"..."}
│   ├── education.json         # {"count":0,"indicators":[],"message":"..."}
│   ├── safety.json            # {"count":0,"indicators":[],"message":"..."}
│   ├── government.json        # {"count":0,"indicators":[],"message":"..."}
│   ├── housing.json           # {"count":0,"indicators":[],"message":"..."}
│   ├── transportation.json    # {"count":0,"indicators":[],"message":"..."}
│   ├── environment.json       # {"count":0,"indicators":[],"message":"..."}
│   │
│   └── volusia_business.json  # Different structure (source, sourceUrl, fetchedAt)
│   └── volusia_gis.json       # Different structure
│
├── gamification/              # Gamification state files
│   ├── zqmco.json             # User state for zqmco
│   ├── test_user.json         # Test user state
│   ├── leaderboard-2026-W35.json  # Weekly leaderboard
│   └── leaderboard-2026-W36.json  # Weekly leaderboard
│
├── climate.json               # Climate data (different structure from cache/)
├── demographics.json          # Demographics data (different structure)
├── economic.json              # Economic data (different structure)
├── indicators.json            # Indicators data (same structure as cache/)
├── map-layers.json            # Map layers data
├── datasets.json              # Datasets data (same as cache/datasets.json)
├── tourism.json               # Tourism data (same as cache/tourism.json)
├── news.json                  # News data (same as cache/news.json)
├── stakeholders.json          # Stakeholder data
├── health.json                # Health check data
├── volusia_employers.db       # Separate SQLite DB for employer data
├── volusia_employers.sql      # SQL dump
├── volusia_employers_v2.sql   # SQL dump v2
├── employers_export.json      # Employer export
├── employers_export.json      # Employer export (duplicate?)
├── volusia_jobs_with_contacts.csv  # Jobs data
│
├── DATA_DICTIONARY.md         # Data field definitions
├── DATA_SOURCES.md            # Data source documentation
├── RECON_REPORT.md            # Reconnaissance report
├── RECON_REPORT_V2.md         # Reconnaissance report v2
└── RECON_REPORT_V3.md         # Reconnaissance report v3 (50+ data sources)
```

### Nginx Configuration

```
nginx/
├── nginx.conf                 # Main nginx config (worker_processes, gzip, etc.)
└── conf.d/default.conf        # Server blocks for all subdomains
                               # server_name: zqmlabs.com, www.zqmlabs.com, data.zqmlabs.com
                               #
                               # Key location blocks:
                               #   /indicators → proxy_pass http://127.0.0.1:8000/indicators
                               #   /api/       → proxy_pass http://127.0.0.1:8000/
                               #   /gamification → proxy_pass http://127.0.0.1:8000/gamification
                               #   /health     → proxy_pass http://127.0.0.1:8000/health
                               #   /data/*.json → proxy_pass http://127.0.0.1:8000/data/$1.json
                               #   /data       → return 301 /data/
                               #   /           → try_files /index.html /index.html (SPA fallback)
                               #   /assets/*   → static files
                               #   /sitemap.xml, /robots.txt, /rss.xml, /manifest.json → static
```

### Build Configuration

```
package.json                   # Vite build config, dependencies
vite.config.ts                 # Vite configuration (build, plugins, aliases)
tsconfig.json                  # TypeScript configuration
tsconfig.node.json             # Node.js TypeScript config
tailwind.config.js             # Tailwind CSS configuration
postcss.config.js              # PostCSS configuration
uv.lock                        # UV lock file (Python dependencies)
pyproject.toml                 # Python project configuration
pytest.ini                     # Pytest configuration
.gitignore                     # Git ignore rules
.dockerignore                  # Docker ignore rules
```

### Scripts and Tools

```
scripts/
├── refresh_v2.py              # Unified data pipeline fetcher + normalizer
│                              # Calls multiple scrapers, normalizes to indicators format
│                              # Writes to data/cache/*.json and volusia.db
│                              # Known issues: doesn't create tables, -888888888 bug
├── refresh_and_diagnose.sh    # Refresh + diagnostics script
├── data_pipeline.py           # Alternative data pipeline
├── scraper.py                 # Base scraper module
├── contribute.py              # Contribution script
├── generate_employer_reports.py  # Employer report generator
├── kb_bridge.py               # Knowledge base bridge
├── backup_db.sh               # Database backup script
└── requirements.txt           # Python requirements for scripts

Tools/
├── verify_data.py             # Data verification script
├── DATA_VERIFICATION_CHECKLIST.md  # Data verification checklist
└── README.md                  # Tools documentation
```

### GitHub Configuration

```
.github/
├── dependabot.yml             # Dependabot configuration
├── ISSUE_TEMPLATE/
│   ├── bug_report.yml         # Bug report template
│   └── feature_request.yml    # Feature request template
└── workflows/
    ├── ci.yml                 # CI pipeline
    └── deploy.yml             # Deployment pipeline
```

---

## Data Flow Summary

```
1. Browser loads / → App.tsx → HomePage.tsx
2. HomePage calls: useEconomicIndicators(), useDemographicIndicators(),
   useClimateIndicators(), useMapLayers(), useDatasets()
3. Each hook calls fetch('/data/{name}.json')
4. Nginx proxies /data/{name}.json → backend :8000/data/{name}.json
5. Backend main.py GET /data/{name}.json reads data/cache/{name}.json
6. JSON response sent back through nginx → browser → React renders

7. Data refresh: POST /refresh?secret=<token>
   → backend main.py trigger_refresh() runs scripts/refresh_v2.py
   → refresh_v2.py fetches from public APIs, normalizes, writes to data/cache/ and volusia.db
```

---

## Known Bugs in Data Flow

| # | Bug | Location | Impact |
|---|-----|----------|--------|
| 1 | `/data/indicators.csv` returns 404 | nginx `location ~ ^/data/(.+)\.json$` only matches `.json` | Download CSV button broken |
| 2 | `/news.json` returns 404 | No `/news.json` route in main.py | NewsPage shows empty/error |
| 3 | `per_capita_income_acs = -888888888` | data/cache/economic.json | HomePage shows -$888M |
| 4 | `pct_white_alone_acs = 579622.0` | data/cache/demographics.json | ResidentsPage shows population count as percentage |
| 5 | `gamification/scoring.py` not imported | backend/main.py | All `/gamification/missions`, `/contribute`, etc. return 404 |
| 6 | `REFRESH_TOKEN` default is `change-me` | backend/main.py line 17 | `/refresh` POST effectively unauthenticated |
| 7 | CORS allows `*` | backend/main.py | Any website can read Volusia data |
| 8 | `datasets` table has empty content | data/cache/datasets.json | Data Explorer shows no content |
| 9 | `cvb_hotels` table has 0 rows | volusia.db | Tourism hotel data empty |
| 10 | 9 demographic indicators stale (2022-2023) | data/cache/demographics.json | Inconsistent vintage with economic (2024) |
| 11 | 19 cache files not in dist/ | build config | Static data missing from build output |
| 12 | `pulse.json` returns stale data | backend/main.py `_get_pulse_data()` | Gamification shows 48h old data |
| 13 | `useLeaderboard()` data structure | backend/gamification.py | Returns `{leaderboard: [...], count: N}` but code may treat as array |
| 14 | `/refresh` GET has no auth | backend/main.py line 136 | Diagnostics accessible without token |
| 15 | `location ~ ^/data/(.+)\.json$` pattern | nginx default.conf | `/data/indicators.csv` doesn't match `.json` pattern |
