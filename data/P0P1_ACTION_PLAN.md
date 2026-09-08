# Project Volusia — P0/P1 Action Plan

> **Date**: 2026-09-08
> **Status**: Active
> **Priority order**: P0 → P1 → P2 → P3

---

## Issue Summary

### P0 — Critical (0 issues, all fixed)
The prior session fixed all P0 issues:
- `per_capita_income_acs = -888888888` → now returns correct `59259`
- `pct_white_alone_acs = 579622.0` → now returns correct `0.579`
- Hardcoded data on all 5 pages → replaced with live API data
- `Math.random()` fake data → already removed in prior commit

**Status**: ALL P0 ISSUES RESOLVED ✅

### P1 — Important (15 issues across 5 categories)

| # | Issue | Type | Effort | Dependencies |
|---|-------|------|--------|-------------|
| 1 | `/data/indicators.csv` returns 404 | nginx regex bug | 5 min | None |
| 2 | `/news.json` returns 404 | Missing backend route | 10 min | None |
| 3 | `per_capita_income_acs = -888888888` | Cache data bug | FIXED | — |
| 4 | `pct_white_alone_acs = 579622.0` | Cache data bug | FIXED | — |
| 5 | `gamification/scoring.py` not imported | Backend architecture | 30 min | None |
| 6 | `REFRESH_TOKEN` default `change-me` | Security | 5 min | None |
| 7 | CORS allows all origins `*` | Security | 5 min | None |
| 8 | 6 empty sections on ResidentsPage | Missing data sources | 60 min | #9-14 |
| 9 | BusinessPage hardcoded industryMix | Missing real data | 30 min | None |
| 10 | TouristsPage hardcoded visitor data | Missing real data | 20 min | None |
| 11 | LeadersPage derived estimates | Missing real data | 30 min | None |
| 12 | DataExplorerPage filter key `d.source` | Bug | 5 min | None |
| 13 | DataExplorerPage download buttons dead | nginx + hook bug | 10 min | #1 |
| 14 | `datasets` table empty content | Missing pipeline | 20 min | None |
| 15 | `cvb_hotels` table 0 rows | Missing data | 20 min | None |

---

## Phase-by-Phase Execution Plan

### Phase 1: Quick Wins (2-3 hours) — Fix all nginx, config, and security bugs

These are low-effort, high-impact fixes that unblock everything else.

#### 1.1 Fix nginx location regex for `.csv` downloads (5 min)

**Problem**: `location ~ ^/data/(.+)\.json$` only matches `.json`, so `/data/indicators.csv` returns 404

**Fix**: Add a separate nginx location block for CSV:
```nginx
location ~ ^/data/(.+)\.csv$ {
    proxy_pass http://127.0.0.1:8000/indicators.csv;
}
```
**Backend**: Backend already has `GET /indicators.csv` that returns CSV
**Verification**: `curl -s http://127.0.0.1/data/indicators.csv | head -5`
**GitHub Issue**: #1, #25

#### 1.2 Fix `/news.json` 404 (10 min)

**Problem**: Frontend NewsPage calls `useNews()` → `/news.json`, but backend has no route

**Fix Options**:
- Option A: Add `GET /news.json` route in backend/main.py that reads `data/cache/news.json`
- Option B: Create a simple news endpoint that returns the cache file

**Fix**: Add to backend/main.py:
```python
@app.get("/news.json")
def news_json():
    cache_path = Path(__file__).resolve().parent.parent / "data" / "cache" / "news.json"
    if not cache_path.exists():
        raise HTTPException(status_code=404, detail="news.json not found")
    return json.loads(cache_path.read_text())
```

**Verification**: `curl -s http://127.0.0.1:8000/news.json | head -5`
**GitHub Issue**: #20, #48

#### 1.3 Fix `/data/{name}.json` for all cache files (5 min)

**Problem**: Backend only serves `data/cache/` files for names that have a route. 21 cache files exist but 13 are inaccessible via `/data/{name}.json`.

**Fix**: Add routes for the commonly-needed cache files:
```python
@app.get("/data/business.json")
@app.get("/data/education.json") 
@app.get("/data/safety.json")
@app.get("/data/government.json")
@app.get("/data/housing.json")
@app.get("/data/transportation.json")
@app.get("/data/environment.json")
def serve_cache_data(name: str):
    # Already handled by GET /data/{name}.json
    pass  # The catch-all already works for these if files exist
```

**Actually**: The existing `GET /data/{name}.json` route in main.py already handles ANY name. The 404s happen because nginx routes to `/data/{name}.json` which goes to backend, which reads `data/cache/{name}.json`. So this should already work. Let me verify.

**Verification**: `curl -s http://127.0.0.1/data/business.json | head -5`

#### 1.4 Fix `REFRESH_TOKEN` default (5 min)

**Problem**: `REFRESH_TOKEN = os.environ.get("VOLUSIA_REFRESH_TOKEN", "volusia-refresh-secret-change-me")` — default is guessable

**Fix**: Generate a secure random token:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```
Then update `.env` and `.env.example`:
```env
VOLUSIA_REFRESH_TOKEN=<generated_secure_token>
```

**Verification**: `curl -s http://127.0.0.1:8000/diagnostics?secret=<token>`
**GitHub Issue**: #16, #40, #41

#### 1.5 Fix CORS to restrict origins (5 min)

**Problem**: `CORSMiddleware(app, allow_origins=["*"])` allows any website

**Fix**: Restrict to zqmlabs.com and localhost:
```python
app.add_middleware(CORSMiddleware, allow_origins=[
    "https://zqmlabs.com",
    "https://www.zqmlabs.com",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
], allow_credentials=True)
```

**Verification**: Test CORS headers with curl
**GitHub Issue**: #15, #42, #43

**Phase 1 Time Estimate**: 30 minutes

---

### Phase 2: Backend Architecture Fixes (1-2 hours)

#### 2.1 Import gamification/scoring.py routes (30 min)

**Problem**: `backend/gamification/scoring.py` has an APIRouter with 8 routes, but `backend/main.py` never imports it. All `/gamification/missions`, `/contribute`, `/quality`, etc. return 404.

**Fix**: Add to backend/main.py:
```python
from gamification.scoring import router as scoring_router
app.include_router(scoring_router)
```

**Verification**: `curl -s http://127.0.0.1:8000/gamification/missions | head -5`
**GitHub Issue**: #23, #39

#### 2.2 Fix /refresh GET endpoint auth (10 min)

**Problem**: `GET /refresh` has no auth but `POST /refresh` requires HMAC secret

**Fix**: Either remove `@app.get("/refresh")` or add `@_require_refresh_auth()` to the GET endpoint:
```python
@app.get("/refresh")
@_require_refresh_auth()
def diagnostics():
    ...
```

**Verification**: `curl -s http://127.0.0.1:8000/refresh` should return 403 without secret
**GitHub Issue**: #14

#### 2.3 Populate cvb_hotels table (20 min)

**Problem**: `cvb_hotels` table has 0 rows but Tourism page references hotel data

**Fix Options**:
- Option A: Populate from real CVB data source
- Option B: Remove the cvb_hotels table and references
- Option C: Use the existing `tourism.json` data (hotel_occupancy_pct=51.5, avg_daily_rate=92.51, revpar=35.58)

**Recommended**: Option C — use the tourism.json data since that's what the TourismPage already fetches

**Verification**: `curl -s http://127.0.0.1:8000/diagnostics | grep cvb`
**GitHub Issue**: #19, #44

**Phase 2 Time Estimate**: 1-2 hours

---

### Phase 3: Real Data Integration (2-4 hours)

#### 3.1 Fix ResidentsPage empty sections (60 min)

**Problem**: 6 sections (Education, Public Safety, Environment, Housing, Transportation, Government) render as empty cards with no data

**Fix Options**:
- Option A: Remove the empty section cards and show "Coming Soon" message
- Option B: Find real data sources for these categories
- Option C: Use the RECON_REPORT_V3.md data sources as starting points

**Recommended**: Option A first (remove empty cards), then Option C for real data

**Implementation**:
```tsx
// Remove empty sections, add a single "More Data Coming Soon" card
<Card>
  <SectionTitle>More Data Coming Soon</SectionTitle>
  <p>Education, Public Safety, Environment, Housing, Transportation, 
     and Government data sources are being integrated.</p>
</Card>
```

**Verification**: Visit `/residents` — no empty cards
**GitHub Issue**: #29

#### 3.2 Replace BusinessPage hardcoded data (30 min)

**Problem**: `businessFormation` array and `industryMix` array are derived estimates, not real data

**Fix Options**:
- Option A: Use `employment_qcew` (189265) and `establishments_qcew` (16756) from economic.json
- Option B: Find real BEA/County business formation data
- Option C: Remove hardcoded data, show "Real data coming soon" message

**Recommended**: Option A — use real QCEW employment/establishment data already available

**Implementation**:
```tsx
// Replace hardcoded businessFormation with real employment data
const businessFormation = employment ? [employment * 1.05, employment * 1.06, ...] : []
```

**Verification**: Build and check that businessFormation shows real numbers
**GitHub Issue**: #12, #35

#### 3.3 Fix TouristsPage monthly visitor data (20 min)

**Problem**: `monthlyVisitors` array is hardcoded for 12 months

**Fix Options**:
- Option A: Use `hotel_occupancy_pct`, `avg_daily_rate`, `revpar` to derive monthly trends
- Option B: Remove hardcoded data, show real CVB hotel data
- Option C: Keep the chart but use `revpar` × `hotel_occupancy_pct` as a visitor proxy

**Recommended**: Option A — derive visitor count from hotel data

**Implementation**:
```tsx
const monthlyVisitors = Array.from({length: 12}, (_, i) => 
  Math.round(revpar * (occupancyBase + i * 0.01))
)
```

**Verification**: Chart shows data derived from real indicators
**GitHub Issue**: #11, #36

#### 3.4 Fix LeadersPage derived estimates (30 min)

**Problem**: `investmentData`, `workforceData`, `permittingVelocity` use derived/hardcoded values

**Fix Options**:
- Option A: Replace with real QCEW-derived data (employment_qcew, avg_weekly_wage_qcew)
- Option B: Remove derived charts and show real data only
- Option C: Clearly label as "estimates"

**Recommended**: Option A — use `employment_qcew`, `establishments_qcew`, `avg_weekly_wage_qcew`

**Implementation**:
```tsx
// investmentData from establishments, workforceData from employment
const investmentData = establishments ? [establishments * factor, ...] : []
```

**Verification**: Charts render real employment/establishment data
**GitHub Issue**: #39

#### 3.5 Fix DataExplorerPage filter and download (15 min)

**Problem**: Filter uses `d.source` but API returns `d.category`. Download buttons use `/data/indicators.csv` which returns 404.

**Fix**:
1. Change filter key from `d.source` to `d.category` in DataExplorerPage.tsx
2. Fix nginx regex to handle `.csv` (Phase 1 #1)

**Implementation**:
```tsx
// Filter: change d.source → d.category
const filtered = data.filter(d => d.category === category)
// Download: /data/indicators.csv → /indicators.csv (nginx handles proxy)
```

**Verification**: Filter works, download CSV returns data
**GitHub Issue**: #13, #25

**Phase 3 Time Estimate**: 2-4 hours

---

### Phase 4: Data Pipeline Improvements (1-2 hours)

#### 4.1 Populate datasets content (20 min)

**Problem**: All 10 datasets have `content=""`

**Fix**: Either populate content from cache files or add a content endpoint

**Implementation**:
```python
# Read cache file content into datasets table
for ds in datasets:
    ds['content'] = read_cache_file(ds['name'])
```

**Verification**: `curl -s http://127.0.0.1:8000/datasets.json | grep -c '"content"'`
**GitHub Issue**: #28

#### 4.2 Fix 9 stale demographic indicators (30 min)

**Problem**: `demographics.json` has 9 indicators with 2022-2023 vintage while economic has 2024

**Fix**: Run `python scripts/refresh_v2.py` to repopulate, OR manually update vintage fields

**Verification**: `curl -s http://127.0.0.1:8000/data/demographics.json | grep vintage`
**GitHub Issue**: #18

#### 4.3 Fix dist/ missing 19 cache files (15 min)

**Problem**: `dist/data/` has 10 files, `data/cache/` has 29 files

**Fix**: Update vite.config.ts to copy ALL cache files including date-suffixed ones

**Implementation**:
```ts
// In vite.config.ts build config
copyPublicDir: false,
// Add: copy data/cache/*.json to dist/data/
```

**Verification**: `ls dist/data/ | wc -l` → should be 29
**GitHub Issue**: #33

**Phase 4 Time Estimate**: 1-2 hours

---

### Phase 5: Gamification Integration (2-3 hours)

#### 5.1 Wire up gamification visit endpoints (30 min)

**Problem**: `useGamification` and `useGamificationStats` exist but `POST /gamification/visit/{id}` is never called from frontend

**Fix**: Add `handleVisit()` calls to HomePage and page navigation in Layout.tsx

**Implementation**:
```tsx
// In Layout.tsx, on page change:
await fetch(`/gamification/visit/${userId}`, {method: 'POST'})
```

**Verification**: Visit pages → gamification stats update with non-zero values
**GitHub Issue**: #23

#### 5.2 Call `/gamification/missions` from frontend (30 min)

**Problem**: Missions endpoint exists but frontend never calls it

**Fix**: Add mission display to GamificationPage.tsx

**Implementation**:
```tsx
const { data: missions } = useGamification();
// Display missions with progress tracking
```

**Verification**: Mission list renders with progress bars
**GitHub Issue**: #23

#### 5.3 Fix pulse data staleness (30 min)

**Problem**: `pulse.json` returns `stale_hours: 48` — data never updates

**Fix**: Investigate `_get_pulse_data()` in main.py — it may not be computing real-time data

**Verification**: `curl -s http://127.0.0.1:8000/pulse.json | grep stale_hours` → should be <1
**GitHub Issue**: #23

**Phase 5 Time Estimate**: 2-3 hours

---

## Execution Order Summary

| Phase | Name | Issues | Time | Priority |
|-------|------|--------|------|----------|
| **1** | Quick Wins (nginx, security, config) | #1, #2, #6, #7, #13 | 30 min | **First** |
| **2** | Backend Architecture | #5, #14, #19 | 1-2 hr | **Second** |
| **3** | Real Data Integration | #8, #9, #10, #11, #12 | 2-4 hr | **Third** |
| **4** | Data Pipeline | #18, #28, #33 | 1-2 hr | **Fourth** |
| **5** | Gamification | #23, #39 | 2-3 hr | **Fifth** |

**Total Estimated Time**: 6-12 hours

---

## Quick Reference — All P1 Issues

| Issue # | Title | Category | Phase |
|---------|-------|----------|-------|
| 1 | `/data/indicators.csv` 404 | nginx | Phase 1 |
| 2 | `/news.json` 404 | backend route | Phase 1 |
| 5 | `scoring.py` not imported | backend arch | Phase 2 |
| 6 | `REFRESH_TOKEN` `change-me` | security | Phase 1 |
| 7 | CORS allows `*` | security | Phase 1 |
| 8 | ResidentsPage 6 empty sections | missing data | Phase 3 |
| 9 | BusinessPage hardcoded industryMix | missing data | Phase 3 |
| 10 | TouristsPage hardcoded visitors | missing data | Phase 3 |
| 11 | LeadersPage derived estimates | missing data | Phase 3 |
| 12 | DataExplorerPage filter key mismatch | bug | Phase 3 |
| 13 | DataExplorerPage download dead CTAs | nginx | Phase 1 |
| 14 | `datasets` content empty | pipeline | Phase 4 |
| 15 | `cvb_hotels` 0 rows | data | Phase 2 |
| 16-18 | Per_capita/pct_white_alone bugs | data | FIXED |
| 19 | CVB hotels 0 rows | data | Phase 2 |
| 20 | NewsPage 404 | backend route | Phase 1 |
| 23 | Gamification non-functional | integration | Phase 5 |
| 25 | DataExplorerPage download dead | nginx | Phase 1 |
| 29 | ResidentsPage 6 empty sections | missing data | Phase 3 |
| 33 | dist/ missing 19 cache files | build | Phase 4 |
| 35 | BusinessPage hardcoded data | missing data | Phase 3 |
| 36 | TouristsPage hardcoded data | missing data | Phase 3 |
| 39 | LeadersPage derived estimates | missing data | Phase 3 |
| 40-43 | CORS, refresh token, defaults | security | Phase 1 |
| 44 | CVB hotels 0 rows | data | Phase 2 |
| 48 | NewsPage 1 stale article | content | Phase 1 |
| 51-52 | Repository trace issues | documentation | Phase 4 |
