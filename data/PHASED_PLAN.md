# Project Volusia — P0/P1 Action Plan

> **Date**: 2026-09-08
> **Status**: Planning

---

## Investigation Results (Live Verification)

After live investigation, the following was confirmed:

| Finding | Status | Notes |
|---------|--------|-------|
| `per_capita_income_acs` | **FIXED** | Now returns `59259` from economic.json |
| `pct_white_alone_acs` | **FIXED** | Now returns `0.579` from indicators.json |
| `scoring.py` routes | **ALREADY IMPORTED** | main.py uses `importlib` to load scoring.py at runtime |
| `GET /gamification/missions` | **WORKS** | Returns 422 (needs contributor_id) — NOT 404 |
| `GET /gamification/pulse` | **WORKS** | Returns data but all stale_hours: 48 |
| `GET /gamification/leaderboard` | **WORKS** | Returns 2 users, both 0 XP |
| `/data/business.json` | **WORKS** | Returns empty message (FL DOE/NCES restructured) |
| `/data/education.json` | **WORKS** | Returns empty message |
| `/data/safety.json` | **WORKS** | Returns empty message |
| `/data/government.json` | **WORKS** | Returns empty message |
| `/data/housing.json` | **WORKS** | Returns empty message |
| `/data/transportation.json` | **WORKS** | Returns empty message |
| `/data/environment.json` | **WORKS** | Returns empty message |
| `/indicators.csv` | **WORKS** | Returns full CSV at `/indicators.csv` (not `/data/`) |
| `/data/indicators.csv` | **404** | Nginx regex `\.json$` doesn't match `.csv` |
| `/news.json` | **404** | Backend has no route for this |
| `cvb_hotels` table | **0 rows** | Confirmed in diagnostics |
| `datasets` content | **ALL EMPTY** | All 10 datasets have `content=""` |

---

## Revised Phase Plan

### Phase 1: Quick Fixes (30 min) — 3 changes

#### 1.1 Fix nginx `.csv` proxy (5 min)
**Problem**: `location ~ ^/data/(.+)\.json$` only matches `.json`. `/data/indicators.csv` returns 404.

**Fix**: Add nginx location block to default.conf:
```nginx
location ~ ^/data/(.+)\.csv$ {
    proxy_pass http://127.0.0.1:8000/indicators.csv;
}
```

**Verification**: `curl -s http://127.0.0.1/data/indicators.csv | head -3`
**Issues fixed**: #1, #25

#### 1.2 Add `/news.json` route (10 min)
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
1. Update `backend/main.py` CORS middleware:
```python
app.add_middleware(CORSMiddleware, allow_origins=[
    "https://zqmlabs.com", "https://www.zqmlabs.com",
    "http://localhost:8080", "http://127.0.0.1:8080",
], allow_credentials=True)
```
2. Generate secure token: `python3 -c "import secrets; print(secrets.token_hex(32))"`
3. Update `.env`: `VOLUSIA_REFRESH_TOKEN=<generated_token>`
4. Update `backend/.env` with same token

**Verification**: `curl -s -I http://127.0.0.1:8000/health | grep -i access-control`
**Issues fixed**: #6, #7, #15, #16, #40, #41, #42, #43

**Phase 1 Time**: 25 min

---

### Phase 2: Data Pipeline & Backend (55 min)

#### 2.1 Fix `/refresh` GET auth (5 min)
**Problem**: `GET /refresh` has no auth but `POST /refresh` requires HMAC secret.

**Fix**: Remove `@app.get("/refresh")` decorator from diagnostics function OR add `@_require_refresh_auth()`.

**Verification**: `curl -s http://127.0.0.1:8000/refresh` → should return 403 without auth
**Issues fixed**: #14

#### 2.2 Fix cvb_hotels empty table (20 min)
**Problem**: `cvb_hotels` table has 0 rows. Tourism page needs hotel data.

**Fix**: The TourismPage already fetches from `/economic.json` which has `hotel_occupancy_pct=51.5`, `avg_daily_rate=92.51`, `revpar=35.58`. The `cvb_hotels` table is redundant. Either:
- Remove the cvb_hotels query from diagnostics, OR
- Populate it from tourism.json

**Verification**: `curl -s http://127.0.0.1:8000/diagnostics | grep -i cvb`
**Issues fixed**: #19, #44

#### 2.3 Populate datasets content (20 min)
**Problem**: All 10 datasets have `content=""`.

**Fix**: For each dataset in `data/cache/datasets.json`, populate `content` from the corresponding cache file.

**Verification**: `curl -s http://127.0.0.1:8000/data/datasets.json | grep -c '"content"'`
**Issues fixed**: #14 (partially), #28

**Phase 2 Time**: 55 min

---

### Phase 3: Real Data Integration (2.5-4 hours)

#### 3.1 Fix ResidentsPage empty sections (60 min)
**Problem**: 6 sections (Education, Safety, Environment, Housing, Transportation, Government) show empty cards.

**Reality**: These categories return `{"count":0,"indicators":[],"message":"Source data unavailable"}`. No data exists.

**Fix**: Replace 6 empty section cards with a single "More Data Coming Soon" card in ResidentsPage.tsx.

**Verification**: Visit `/residents` — no empty cards
**Issues fixed**: #8, #29

#### 3.2 Replace BusinessPage hardcoded data (30 min)
**Problem**: `businessFormation` and `industryMix` arrays are derived estimates.

**Reality**: Backend has `employment_qcew=189265`, `establishments_qcew=16756` from `/economic.json`.

**Fix**: Use real QCEW data for business formation and industry mix charts.

**Verification**: BusinessPage shows real numbers
**Issues fixed**: #9, #12, #35

#### 3.3 Fix TouristsPage hardcoded visitor data (20 min)
**Problem**: `monthlyVisitors` array is hardcoded.

**Reality**: Backend has `hotel_occupancy_pct=51.5`, `avg_daily_rate=92.51`, `revpar=35.58`.

**Fix**: Derive visitor trends from real hotel data.

**Verification**: Chart shows data derived from indicators
**Issues fixed**: #10, #11, #36

#### 3.4 Fix LeadersPage derived estimates (30 min)
**Problem**: `investmentData`, `workforceData`, `permittingVelocity` use derived/hardcoded values.

**Reality**: Backend has `employment_qcew=189265`, `establishments_qcew=16756`, `avg_weekly_wage_qcew=1041`.

**Fix**: Use real QCEW data for all charts.

**Verification**: Charts show real employment/establishment data
**Issues fixed**: #11, #39

#### 3.5 Fix DataExplorerPage filter key (5 min)
**Problem**: Filter uses `d.source` but API returns `d.category`.

**Fix**: Change `d.source` → `d.category` in DataExplorerPage.tsx.

**Verification**: Filter works correctly
**Issues fixed**: #12, #13, #25

**Phase 3 Time**: 2.5-4 hours

---

### Phase 4: Gamification Integration (2-3 hours)

#### 4.1 Wire up gamification visit tracking (30 min)
**Problem**: `useGamification` exists but `POST /gamification/visit/{id}` never called from frontend.

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

**Fix**: Investigate `_get_pulse_data()` in main.py — it may need to compute real-time data.

**Verification**: `curl -s http://127.0.0.1:8000/pulse.json | grep stale_hours` → should be <1
**Issues fixed**: #23

#### 4.3 Add missions display to GamificationPage (30 min)
**Problem**: Missions exist in backend but frontend never calls `/gamification/missions`.

**Fix**: Add mission display to GamificationPage.tsx.

**Verification**: Mission list renders with progress bars
**Issues fixed**: #23

**Phase 4 Time**: 2-3 hours

---

### Phase 5: Build & Distribution (15 min)

#### 5.1 Fix dist/ missing 19 cache files (15 min)
**Problem**: `dist/data/` has 10 files, `data/cache/` has 29.

**Fix**: Update vite.config.ts to copy ALL cache files including date-suffixed ones.

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

**Total**: 6-8 hours across 5 phases.

---

## Quick Start: Phase 1 Commands

```bash
# 1. Fix nginx .csv proxy
# Add to /c/Users/zqmco/scoop/apps/nginx/current/conf/conf.d/default.conf:
# location ~ ^/data/(.+)\.csv$ {
#     proxy_pass http://127.0.0.1:8000/indicators.csv;
# }
# Then: taskkill /f /im nginx.exe && start nginx

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

---

## All P1 Issues Reference

| Issue # | Title | Category | Phase |
|---------|-------|----------|-------|
| 1 | `/data/indicators.csv` 404 | nginx | Phase 1 |
| 2 | `/news.json` 404 | backend route | Phase 1 |
| 5 | `scoring.py` not imported | backend arch | ALREADY FIXED (importlib) |
| 6 | `REFRESH_TOKEN` `change-me` | security | Phase 1 |
| 7 | CORS allows `*` | security | Phase 1 |
| 8 | ResidentsPage 6 empty sections | missing data | Phase 3 |
| 9 | BusinessPage hardcoded industryMix | missing data | Phase 3 |
| 10 | TouristsPage hardcoded visitors | missing data | Phase 3 |
| 11 | LeadersPage derived estimates | missing data | Phase 3 |
| 12 | DataExplorerPage filter key mismatch | bug | Phase 3 |
| 13 | DataExplorerPage download dead CTAs | nginx | Phase 1 |
| 14 | `datasets` content empty | pipeline | Phase 2 |
| 15 | `cvb_hotels` 0 rows | data | Phase 2 |
| 16-18 | Per_capita/pct_white_alone bugs | data | FIXED |
| 19 | CVB hotels 0 rows | data | Phase 2 |
| 20 | NewsPage 404 | backend route | Phase 1 |
| 23 | Gamification non-functional | integration | Phase 4 |
| 25 | DataExplorerPage download dead | nginx | Phase 1 |
| 29 | ResidentsPage 6 empty sections | missing data | Phase 3 |
| 33 | dist/ missing 19 cache files | build | Phase 5 |
| 35 | BusinessPage hardcoded data | missing data | Phase 3 |
| 36 | TouristsPage hardcoded data | missing data | Phase 3 |
| 39 | LeadersPage derived estimates | missing data | Phase 3 |
| 40-43 | CORS, refresh token, defaults | security | Phase 1 |
| 44 | CVB hotels 0 rows | data | Phase 2 |
| 48 | NewsPage 1 stale article | content | Phase 1 |
| 51-52 | Repository trace issues | documentation | Phase 4 |

---

## Documents Created

- `data/REPOSITORY_TRACE.md` — Full file-by-file trace with architecture diagram
- `data/P0P1_ACTION_PLAN.md` — Detailed action plan with code snippets
- `data/PHASED_PLAN.md` — Phased execution plan with live verification
- `data/AUDIT_2026-09-08.md` — Full audit log of 48 issues
- `data/issue_template_*.md` — Individual issue templates for GitHub
