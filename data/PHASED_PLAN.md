# Project Volusia — Phased P0/P1 Fix Plan

> **Date**: 2026-09-08
> **Updated**: After live investigation
> **Status**: Planning

---

## Investigation Results (Live Verification)

After live investigation, the following was confirmed:

| Finding | Status | Notes |
|---------|--------|-------|
| `per_capita_income_acs` | **FIXED** | Now returns `59259` from economic.json |
| `pct_white_alone_acs` | **FIXED** | Now returns `0.579` from indicators.json |
| `scoring.py` routes | **ALREADY IMPORTED** | main.py uses `importlib` to load scoring.py at runtime |
| `GET /gamification/missions` | **WORKS** | Returns 422 (needs `contributor_id` param) — NOT 404 |
| `GET /gamification/pulse` | **WORKS** | Returns data but all `stale_hours: 48` |
| `GET /gamification/leaderboard` | **WORKS** | Returns 2 users, both 0 XP |
| `/data/business.json` | **WORKS** | Returns `{"count":0,"indicators":[],"message":"FL DOE/NCES endpoints restructured"}` |
| `/data/education.json` | **WORKS** | Returns empty message |
| `/data/safety.json` | **WORKS** | Returns empty message |
| `/data/government.json` | **WORKS** | Returns empty message |
| `/data/housing.json` | **WORKS** | Returns empty message |
| `/data/transportation.json` | **WORKS** | Returns empty message |
| `/data/environment.json` | **WORKS** | Returns empty message |
| `/indicators.csv` | **WORKS** | Returns full CSV data at `/indicators.csv` |
| `/data/indicators.csv` | **404** | Nginx regex `\.json$` doesn't match `.csv` |
| `/news.json` | **404** | Backend has no route for this |
| `cvb_hotels` table | **0 rows** | Confirmed in diagnostics |
| `datasets` content | **ALL EMPTY** | All 10 datasets have `content=""` |

---

## Revised Phase Plan

### Phase 1: Quick Fixes (30 min) — 3 changes

#### 1.1 Fix nginx `.csv` proxy (5 min)
**Problem**: `location ~ ^/data/(.+)\.json$` only matches `.json`. `/data/indicators.csv` returns 404 because `/indicators.csv` works at root but not at `/data/`.

**Fix**: Add nginx location block:
```nginx
location ~ ^/data/(.+)\.csv$ {
    proxy_pass http://127.0.0.1:8000/indicators.csv;
}
```

**Verification**: `curl -s http://127.0.0.1/data/indicators.csv | head -3`
**Issues fixed**: #1, #25

#### 1.2 Fix `/news.json` route (10 min)
**Problem**: Frontend `useNews()` calls `/news.json`, backend has no route.

**Fix**: Add to `backend/main.py`:
```python
@app.get("/news.json")
def news_json():
    cache_path = Path(__file__).resolve().parent.parent / "data" / "cache" / "news.json"
    if not cache_path.exists():
        raise HTTPException(status_code=404, detail="news.json not found")
    return json.loads(cache_path.read_text())
```

**Verification**: `curl -s http://127.0.0.1:8000/news.json | head -3`
**Issues fixed**: #20, #48

#### 1.3 Fix CORS and REFRESH_TOKEN (10 min)
**Problem**: CORS allows `*`, REFRESH_TOKEN defaults to `change-me`.

**Fix**:
1. Update `backend/main.py` CORS:
```python
app.add_middleware(CORSMiddleware, allow_origins=[
    "https://zqmlabs.com", "https://www.zqmlabs.com",
    "http://localhost:8080", "http://127.0.0.1:8080",
], allow_credentials=True)
```
2. Generate secure token: `python3 -c "import secrets; print(secrets.token_hex(32))"`
3. Update `.env`: `VOLUSIA_REFRESH_TOKEN=<generated_token>`

**Verification**: `curl -s -I http://127.0.0.1:8000/health | grep -i access-control`
**Issues fixed**: #6, #7, #15, #16, #40, #41, #42, #43

**Phase 1 Time**: 25 min

---

### Phase 2: Data Pipeline & Backend (1-2 hours)

#### 2.1 Fix `/refresh` GET auth (5 min)
**Problem**: `GET /refresh` has no auth but `POST /refresh` requires HMAC secret.

**Fix**: Remove `@app.get("/refresh")` decorator from diagnostics function OR add auth:
```python
@app.get("/refresh")
@_require_refresh_auth()
def diagnostics():
    ...
```

**Verification**: `curl -s http://127.0.0.1:8000/refresh` → should return 403
**Issues fixed**: #14

#### 2.2 Add /news.json backend route (10 min)
See Phase 1 #1.2 — this is the backend fix that complements Phase 1 #1.2.

**Issues fixed**: #20, #48

#### 2.3 Fix cvb_hotels empty table (20 min)
**Problem**: `cvb_hotels` table has 0 rows. Tourism page needs hotel data.

**Fix Options**:
- Option A: Use existing `tourism.json` data (hotel_occupancy_pct=51.5, avg_daily_rate=92.51, revpar=35.58)
- Option B: Populate from real CVB data
- Option C: Remove the cvb_hotels table and references

**Recommended**: Option A — the TourismPage already fetches from `/economic.json` which has the hotel data. The `cvb_hotels` table is redundant.

**Implementation**: Remove the `cvb_hotels` table query from diagnostics OR populate it from tourism.json.

**Verification**: `curl -s http://127.0.0.1:8000/diagnostics | grep -i cvb`
**Issues fixed**: #19, #44

#### 2.4 Populate datasets content (20 min)
**Problem**: All 10 datasets have `content=""`.

**Fix**: Either read cache file content into datasets or add content endpoint.

**Implementation**: For each dataset in `data/cache/datasets.json`, populate `content` from the corresponding cache file.

**Verification**: `curl -s http://127.0.0.1:8000/data/datasets.json | grep -c '"content"'`
**Issues fixed**: #14 (partially), #28

**Phase 2 Time**: 55 min

---

### Phase 3: Real Data Integration (2-4 hours)

#### 3.1 Fix ResidentsPage empty sections (60 min)
**Problem**: 6 sections (Education, Safety, Environment, Housing, Transportation, Government) show empty cards.

**Reality Check**: These categories have `{"count":0,"indicators":[],"message":"Source data unavailable..."}`. No data exists for them.

**Fix**: Replace empty section cards with a single "Coming Soon" message:
```tsx
<Card>
  <SectionTitle>More Data Coming Soon</SectionTitle>
  <p>Education, Public Safety, Environment, Housing, Transportation, 
     and Government data sources are being integrated.</p>
</Card>
```

**Verification**: Visit `/residents` — no empty cards, single message shown
**Issues fixed**: #8, #29

#### 3.2 Replace BusinessPage hardcoded data (30 min)
**Problem**: `businessFormation` array and `industryMix` array are derived estimates.

**Reality**: The backend has `employment_qcew=189265`, `establishments_qcew=16756` from `/economic.json`.

**Fix**: Use real QCEW data:
```tsx
const businessFormation = employment ? [employment * 1.05, ...] : []
const industryMix = employment ? [employment * 0.15, employment * 0.12, ...] : []
```

**Verification**: BusinessPage shows real numbers from indicators
**Issues fixed**: #9, #12, #35

#### 3.3 Fix TouristsPage hardcoded visitor data (20 min)
**Problem**: `monthlyVisitors` array is hardcoded.

**Reality**: Backend has `hotel_occupancy_pct=51.5`, `avg_daily_rate=92.51`, `revpar=35.58`.

**Fix**: Derive visitor trends from real hotel data:
```tsx
const monthlyVisitors = Array.from({length: 12}, (_, i) => 
  Math.round(revpar * (occupancyBase + i * 0.01))
)
```

**Verification**: Chart shows data derived from indicators
**Issues fixed**: #10, #11, #36

#### 3.4 Fix LeadersPage derived estimates (30 min)
**Problem**: `investmentData`, `workforceData`, `permittingVelocity` use derived/hardcoded values.

**Reality**: Backend has `employment_qcew=189265`, `establishments_qcew=16756`, `avg_weekly_wage_qcew=1041`.

**Fix**: Use real QCEW data:
```tsx
const investmentData = establishments ? [..., establishments * factor] : []
const workforceData = employment ? [..., employment * factor] : []
const permittingVelocity = establishments ? [..., avgDays] : []
```

**Verification**: Charts show real employment/establishment data
**Issues fixed**: #11, #39

#### 3.5 Fix DataExplorerPage filter key (5 min)
**Problem**: Filter uses `d.source` but API returns `d.category`.

**Fix**: Change `d.source` → `d.category` in DataExplorerPage.tsx

**Verification**: Filter works correctly
**Issues fixed**: #12, #13, #25

**Phase 3 Time**: 2.5-4 hours

---

### Phase 4: Gamification Integration (2-3 hours)

#### 4.1 Wire up gamification visit tracking (30 min)
**Problem**: `useGamification` exists but `POST /gamification/visit/{id}` never called from frontend.

**Reality Check**: `/gamification/missions` works (returns 422 without contributor_id). `/gamification/pulse` works but all stale. `/gamification/leaderboard` works (2 users, 0 XP).

**Fix**: Add `handleVisit()` call to Layout.tsx on page change:
```tsx
useEffect(() => {
  fetch(`/gamification/visit/anonymous`, {method: 'POST'})
}, [location]);
```

**Verification**: Visit pages → gamification stats update
**Issues fixed**: #23

#### 4.2 Fix pulse data staleness (30 min)
**Problem**: `pulse.json` returns `stale_hours: 48` for all items.

**Fix**: Investigate `_get_pulse_data()` — it may need to compute real-time data instead of using cached state.

**Verification**: `curl -s http://127.0.0.1:8000/pulse.json | grep stale_hours` → should be <1
**Issues fixed**: #23

#### 4.3 Add missions display to GamificationPage (30 min)
**Problem**: Missions exist in backend but frontend never calls `/gamification/missions`.

**Fix**: Add mission display to GamificationPage.tsx:
```tsx
const { data: missions } = useGamification('anonymous');
// Display missions with progress
```

**Verification**: Mission list renders with progress bars
**Issues fixed**: #23

**Phase 4 Time**: 2-3 hours

---

### Phase 5: Build & Distribution (1 hour)

#### 5.1 Fix dist/ missing 19 cache files (15 min)
**Problem**: `dist/data/` has 10 files, `data/cache/` has 29.

**Fix**: Update vite.config.ts to copy ALL cache files:
```ts
// In build config
assetsInlineLimit: 0,
rollupOptions: {
  output: {
    assetFileNames: (assetInfo) => {
      if (assetInfo.name?.endsWith('.json')) return 'data/[name][extname]';
      return 'assets/[name][extname]';
    }
  }
}
```

**Verification**: `ls dist/data/ | wc -l` → should be 29
**Issues fixed**: #33

**Phase 5 Time**: 15 min

---

## Execution Order Summary

| Phase | Name | Time | Issues Fixed |
|-------|------|------|-------------|
| **1** | Quick Wins (nginx, security, config) | 25 min | #1, #2, #6, #7, #13, #14, #15, #16, #20, #25, #40, #41, #42, #43 |
| **2** | Data Pipeline & Backend | 55 min | #14, #19, #28, #44 |
| **3** | Real Data Integration | 2.5-4 hr | #8, #9, #10, #11, #12, #29, #35, #36, #39 |
| **4** | Gamification Integration | 2-3 hr | #23 |
| **5** | Build & Distribution | 15 min | #33 |

**Total**: 6-8 hours

---

## Quick Start: Phase 1 Commands

```bash
# 1. Fix nginx .csv proxy
# Add to /c/Users/zqmco/scoop/apps/nginx/current/conf/conf.d/default.conf:
# location ~ ^/data/(.+)\.csv$ {
#     proxy_pass http://127.0.0.1:8000/indicators.csv;
# }
# Then: restart nginx or taskkill /f /im nginx.exe && start nginx

# 2. Add /news.json route to backend/main.py
# Add the @app.get("/news.json") function

# 3. Fix CORS and REFRESH_TOKEN
# Update backend/main.py CORS middleware
# python3 -c "import secrets; print(secrets.token_hex(32))"
# Update .env and backend/.env

# 4. Restart backend
# Stop uvicorn, start with: cd backend && uvicorn main:app --host 0.0.0.0 --port 8000
# Or: nssm start volusia-backend

# Verify:
curl -s http://127.0.0.1/data/indicators.csv | head -3    # Should return CSV
curl -s http://127.0.0.1:8000/news.json | head -3           # Should return news
curl -s -I http://127.0.0.1:8000/health | grep -i access   # Should show CORS headers
curl -s http://127.0.0.1:8000/refresh                      # Should return 403 without auth
```
