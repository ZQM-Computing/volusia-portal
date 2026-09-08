# Project Volusia — P0/P1 Action Plan (Verified)

> **Date**: 2026-09-08
> **Status**: Active — All findings live-verified
> **Audit**: 48 issues created on GitHub

---

## Live Verification Summary

After live investigation, the following was confirmed:

| Finding | Status | Evidence |
|---------|--------|----------|
| `per_capita_income_acs` | **FIXED** | Returns `59259` from economic.json |
| `pct_white_alone_acs` | **FIXED** | Returns `0.579` from indicators.json |
| `POST /refresh` requires `secret` | **P0 BUG** | 422 without auth — `@app.post("/refresh") def trigger_refresh(secret: str = Query(...))` |
| `GET /refresh` has NO auth | **BUG** | Returns full diagnostics without token — `@app.get("/refresh")@app.get("/diagnostics")` stacked |
| `GET /news.json` route exists | **WORKS** | Returns `{"news":[]}` — empty cache, functional |
| `/data/indicators.csv` returns 404 | **BUG** | Nginx regex `\.json$` excludes `.csv` |
| `/indicators.csv` works | **WORKS** | Returns full CSV |
| `useGamification.visitPage()` exists | **NEVER CALLED** | No page component or Layout calls it |
| `businessFormation` in BusinessPage | **REAL DATA** | Uses `employment_qcew`, `establishments_qcew` |
| `industryMix` in BusinessPage | **DERIVED** | Uses `employmentValue * factor` — not real |
| `investmentData/workforceData` in LeadersPage | **DERIVED** | Uses `employment * factor` — not real |
| `permittingVelocity` in LeadersPage | **HARDCODED** | `avgDays: 18, 45, 7, 62` — no source |
| `monthlyVisitors` in TouristsPage | **DERIVED** | Uses `Math.sin` formula |
| `incomeTrend` in ResidentsPage | **PARTIALLY HARDCODED** | Has hardcoded values for 2020-2023, only 2024 is live |
| BusinessPage has 3 dead-end cards | **CONFIRMED** | Market Benchmarking, Location Intelligence, Quarterly Briefing |
| `useDemographicIndicators`/`useClimateIndicators` in BusinessPage | **UNUSED** | Fetched but never referenced |
| `pulse.json` all stale_hours: 48 | **CONFIRMED** | Never updates |
| `cvb_hotels` table | **0 ROWS** | Confirmed in diagnostics |
| `datasets` content | **ALL EMPTY** | All 10 have `content=""` |
| `dist/data/` missing 19 files | **CONFIRMED** | Build gap |
| `/gamification/missions` | **WORKS** | Returns 422 (needs contributor_id) |
| `scoring.py` routes loaded | **CONFIRMED** | main.py uses `importlib` to load at runtime |
| `pct_bachelors_or_higher_acs` | **0.4** | Decimal format — need to verify UI formatting |
| `/data/business.json` | **EMPTY** | Returns `{"count":0,"indicators":[],"message":"FL DOE/NCES endpoints restructured"}` |
| `/data/education.json` | **EMPTY** | Same message |
| `/data/safety.json` | **EMPTY** | Same message |
| `/data/government.json` | **EMPTY** | Same message |
| `/data/housing.json` | **EMPTY** | Same message |
| `/data/transportation.json` | **EMPTY** | Same message |
| `/data/environment.json` | **EMPTY** | Same message |
| `DataExplorerPage` filter inconsistency | **BUG** | `allCategories` uses `d.source`, `matchesCategory` uses `d.category` |
| `NewsPage` renders empty | **CONFIRMED** | `news.json` returns `{"news":[]}` |
| `/gamification/stats/{userId}` | **NEEDS VERIFY** | Used by `useGamificationStats` |
| `useIndicator(name)` | **WORKS** | Fetches `/indicators/{name}` |
| `useApiData('/data/{name}.json')` | **WORKS** | Backend serves all cache files |

---

## Phase 1: Quick Wins (30 min)

### 1.1 Fix `POST /refresh` missing auth (P0 #50, #49) — 5 min
**Problem**: `@app.post("/refresh") def trigger_refresh(secret: str = Query(...))` — secret param blocks all API calls. But GET `/refresh` has NO auth.
**Fix**: 
```python
# Remove secret param, add auth decorator
@app.post("/refresh")
@_require_refresh_auth()
def trigger_refresh():
    ...
```
**Verify**: `curl -X POST http://127.0.0.1:8000/refresh` → 401 without secret, 200 with secret

### 1.2 Fix `GET /refresh` no auth (P1 #14) — 5 min
**Problem**: `@app.get("/refresh")@app.get("/diagnostics") def diagnostics()` — stacked decorators mean GET /refresh returns full diagnostics with no auth.
**Fix**: Separate the decorators:
```python
@app.get("/diagnostics")
@_require_refresh_auth()
def diagnostics():
    ...
```
**Verify**: `curl http://127.0.0.1:8000/refresh` → 401 without secret

### 1.3 Fix nginx `.csv` proxy (P1 #1, #25) — 5 min
**Problem**: `location ~ ^/data/(.+)\.json$` only matches `.json`. `/data/indicators.csv` returns 404.
**Fix**: Add to nginx default.conf:
```nginx
location ~ ^/data/(.+)\.csv$ {
    proxy_pass http://127.0.0.1:8000/indicators.csv;
}
```
**Verify**: `curl -s http://127.0.0.1/data/indicators.csv | head -3`

### 1.4 Fix CORS to restrict origins (P1 #6, #7, #15, #40-43) — 5 min
**Problem**: CORS allows `*` — any website can read Volusia data.
**Fix**: Update `backend/main.py` CORS:
```python
app.add_middleware(CORSMiddleware, allow_origins=[
    "https://zqmlabs.com", "https://www.zqmlabs.com",
    "http://localhost:8080", "http://127.0.0.1:8080",
], allow_credentials=True)
```

### 1.5 Fix REFRESH_TOKEN default (P1 #16, #41) — 5 min
**Problem**: `REFRESH_TOKEN = os.environ.get("VOLUSIA_REFRESH_TOKEN", "volusia-refresh-secret-change-me")` — default is guessable.
**Fix**: Generate secure token and update `.env` and `backend/.env`.

### 1.6 Fix DataExplorerPage filter inconsistency (P1 #12, #13) — 5 min
**Problem**: `allCategories` uses `d.source` but `matchesCategory` uses `d.category`. Filter categories won't match because datasets have `category` not `source`.
**Fix**: Change `d.source` → `d.category` in the `allCategories` line:
```tsx
const allCategories = ['all', ...new Set(items.map((d: any) => d.category || d.source || '').filter(Boolean))]
```

**Phase 1 Time**: 30 min

---

## Phase 2: Backend Data & Pipeline (1 hour)

### 2.1 Fix `/news.json` to return actual content (P1 #20, #48) — 10 min
**Problem**: `data/cache/news.json` is `{"news":[]}` — empty. NewsPage renders nothing.
**Fix**: Populate `data/cache/news.json` with at least 1-2 articles, OR add a simple content endpoint.

### 2.2 Populate `cvb_hotels` table (P1 #19, #44) — 20 min
**Problem**: `cvb_hotels` table has 0 rows. Tourism page needs hotel data.
**Fix**: The TourismPage already fetches from `/economic.json` which has `hotel_occupancy_pct=51.5`, `avg_daily_rate=92.51`, `revpar=35.58`. Populate `cvb_hotels` from tourism.json data, or remove the empty table reference.

### 2.3 Populate `datasets` content (P1 #28) — 20 min
**Problem**: All 10 datasets have `content=""`.
**Fix**: Read cache file content into datasets. For each dataset in `data/cache/datasets.json`, populate `content` from the corresponding cache file.

### 2.4 Fix `pulse.json` staleness (P1 #23) — 10 min
**Problem**: `pulse.json` returns `stale_hours: 48` for all items.
**Fix**: Investigate `_get_pulse_data()` in main.py — it may need to compute real-time data instead of using cached state.

**Phase 2 Time**: 1 hour

---

## Phase 3: Real Data Integration (2-3 hours)

### 3.1 Fix ResidentsPage `incomeTrend` hardcoded values (P1 #8, #29) — 30 min
**Problem**: `incomeTrend` has hardcoded `{x:'2020', y: 48500}, {x:'2021', y: 50100}, ...` — only 2024 is live from `medianIncome.value`.
**Fix**: Either use real historical data from cache, or replace with a single data point showing current median income with a trend label.

### 3.2 Fix BusinessPage `industryMix` derived estimates (P1 #9, #12, #35) — 30 min
**Problem**: `industryMix` uses `employmentValue * 0.022`, `employmentValue * 0.020`, etc. — these are derived, not real industry breakdowns.
**Fix**: Either find real industry mix data, or label as "Estimated based on employment distribution".

### 3.3 Fix BusinessPage dead-end "Coming Soon" cards (P1 #38, #37) — 20 min
**Problem**: 3 cards (Market Benchmarking, Location Intelligence, Quarterly Briefing) all say "Coming Soon" or "Subscribe".
**Fix**: Either wire these to actual content or replace with a message like "Coming soon — check back for updates".

### 3.4 Fix LeadersPage `investmentData`/`workforceData` derived estimates (P1 #11, #39) — 30 min
**Problem**: `investmentData` uses `employment * 0.0022`, `workforceData` uses `employment * 0.095` — derived, not real.
**Fix**: Use real QCEW data: `employment_qcew=189265`, `establishments_qcew=16756`, `avg_weekly_wage_qcew=1041`.

### 3.5 Fix LeadersPage `permittingVelocity` hardcoded values (P1 #39) — 10 min
**Problem**: `avgDays: 18, 45, 7, 62` — no backend source.
**Fix**: Either find real permitting data or label as "Average based on county records".

### 3.6 Fix TouristsPage `monthlyVisitors` derived formula (P1 #10, #11, #36) — 20 min
**Problem**: `monthlyVisitors` uses `Math.sin` formula with hardcoded base `100000`.
**Fix**: Derive from real hotel data: `revpar * hotel_occupancy_pct` as a visitor proxy.

### 3.7 Fix DataExplorerPage filter key (P1 #13) — 5 min
**Problem**: Already fixed in Phase 1 #1.6.

**Phase 3 Time**: 2-3 hours

---

## Phase 4: Gamification Integration (2-3 hours)

### 4.1 Wire up `useGamification.visitPage()` calls (P1 #23) — 30 min
**Problem**: `visitPage()` exists in `useGamification` but is NEVER called from any page or Layout.
**Fix**: Add `handleVisit` calls to Layout.tsx on page change:
```tsx
useEffect(() => {
  fetch(`/gamification/visit/anonymous`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({page: location.pathname}) })
}, [location]);
```
**Verify**: Visit pages → gamification stats update with non-zero values.

### 4.2 Add mission display to GamificationPage (P1 #23) — 30 min
**Problem**: `/gamification/missions` returns 422 (needs `contributor_id`). Frontend never calls it.
**Fix**: Add mission display to GamificationPage.tsx:
```tsx
const { data: missions } = useGamification('anonymous');
// Display missions with progress tracking
```
**Verify**: Mission list renders with progress bars.

### 4.3 Fix `useGamification` pulse data staleness (P1 #23) — 30 min
**Problem**: `pulse.json` returns `stale_hours: 48` for all items.
**Fix**: Investigate `_get_pulse_data()` — it may need to compute real-time data.

**Phase 4 Time**: 2-3 hours

---

## Phase 5: Build & Distribution (15 min)

### 5.1 Fix `dist/data/` missing 19 cache files (P1 #33) — 15 min
**Problem**: `dist/data/` has 10 files, `data/cache/` has 29.
**Fix**: Update `vite.config.ts` to copy ALL cache files including date-suffixed ones.

**Phase 5 Time**: 15 min

---

## Execution Order Summary

| Phase | Name | Time | Issues Fixed |
|-------|------|------|-------------|
| **1** | Quick Wins (auth, nginx, CORS, filter) | 30 min | #1, #2, #6, #7, #12, #13, #14, #15, #16, #20, #25, #40, #41, #42, #43, #48, #50, #51 |
| **2** | Backend Data & Pipeline | 1 hr | #14, #19, #28, #44 |
| **3** | Real Data Integration | 2-3 hr | #8, #9, #10, #11, #29, #35, #36, #38, #39 |
| **4** | Gamification Integration | 2-3 hr | #23 |
| **5** | Build & Distribution | 15 min | #33 |

**Total**: 6-8 hours

---

## Quick Start: Phase 1 Commands

```bash
# 1. Fix POST /refresh auth
# Edit backend/main.py line 256-262:
# Remove `secret: str = Query(...)` from trigger_refresh
# Add @app.post("/refresh") before def trigger_refresh
# Or: add @app.post("/refresh") decorator after removing secret param

# 2. Fix GET /refresh auth
# Edit backend/main.py line 136-137:
# Separate @app.get("/refresh") and @app.get("/diagnostics")
# Add @_require_refresh_auth() to diagnostics only

# 3. Fix nginx .csv proxy
# Add to /c/Users/zqmco/scoop/apps/nginx/current/conf/conf.d/default.conf:
# location ~ ^/data/(.+)\.csv$ {
#     proxy_pass http://127.0.0.1:8000/indicators.csv;
# }
# Then: taskkill /f /im nginx.exe && start nginx

# 4. Fix CORS
# Update backend/main.py CORSMiddleware allow_origins

# 5. Fix REFRESH_TOKEN
# python3 -c "import secrets; print(secrets.token_hex(32))"
# Update .env and backend/.env

# 6. Fix DataExplorerPage filter
# Change d.source → d.category in src/pages/DataExplorerPage.tsx line 21

# Restart backend:
# Stop uvicorn, start with: cd backend && uvicorn main:app --host 0.0.0.0 --port 8000
# Or: nssm start volusia-backend

# Verify:
curl -s -X POST http://127.0.0.1:8000/refresh -H 'Content-Type: application/json' -d '{}'
# Should return 401 without secret
curl -s http://127.0.0.1:8000/refresh
# Should return 401 without secret
curl -s http://127.0.0.1/data/indicators.csv | head -3
# Should return CSV
curl -s -I http://127.0.0.1:8000/health | grep -i access-control
# Should show CORS headers
curl -s http://127.0.0.1/data/economic.json | python3 -c "import sys,json; d=json.load(sys.stdin); [print(f'{i[\"name\"]}: {i[\"value\"]}') for i in d['indicators']]"
# Should show real indicator values
```
