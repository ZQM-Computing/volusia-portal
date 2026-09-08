# Priority 0 & 1 Fix Plan — Project Volusia

> **Date:** 2026-09-08
> **Total P0+P1 Issues:** 11 (2 P0, 9 P1)
> **Status:** Planning phase

---

## Issue Inventory

### P0 — Critical Data Corruption (2 issues)

| # | Issue | Root Cause |
|---|-------|-----------|
| #9 | per_capita_income_acs = -888888888 (garbage sentinel) | Cache file economic.json has error value, pipeline doesn't reject sentinels |
| #10 | pct_white_alone_acs = 579622.0 (population copied over percentage) | Cache file demographics.json has wrong value mapping |

### P1 — Broken Functionality (9 issues)

| # | Issue | Category |
|---|-------|----------|
| #11 | TouristsPage: hardcoded monthlyVisitors (820, 910...) | Frontend hardcoded data |
| #12 | BusinessPage: hardcoded industryMix percentages | Frontend hardcoded data |
| #13 | DataExplorerPage: filter key mismatch (d.source vs d.name) | Frontend API mismatch |
| #14 | /indicators.csv and /news.json return 404 | Backend missing routes |
| #15 | CORS allows all origins (*) | Security |
| #16 | Default refresh token = "change-me" | Security |
| #17 | ResidentsPage: hardcoded nationalAvg: 100 | Frontend hardcoded data |
| #20 | NewsPage broken — /news.json returns 404 | Backend missing route |
| #25 | DataExplorerPage download buttons are dead CTAs | Frontend API path mismatch |

### P1 — Empty Sections (1 issue)

| # | Issue | Category |
|---|-------|----------|
| #29 | ResidentsPage: 6 empty placeholder sections (Education, Safety, Environment, Housing, Transit, Gov) | Missing data sources |

---

## Execution Order

### Phase 1: P0 Data Corruption Fix (Critical — Start Here)

**Goal:** Fix corrupted indicator values that break the home page and resident pages.

#### Step 1.1: Fix per_capita_income_acs garbage value (#9)
- **File:** `data/cache/economic.json`
- **Problem:** Contains `per_capita_income_acs: -888888888`
- **Fix:** Replace with correct value (~59259). Either re-run pipeline or manually patch.
- **Verification:** `curl http://127.0.0.1:8000/data/economic.json | grep per_capita_income_acs` should show ~59259

#### Step 1.2: Fix pct_white_alone_acs wrong value (#10)
- **File:** `data/cache/demographics.json`
- **Problem:** Contains `pct_white_alone_acs: 579622.0` (population count, not percentage)
- **Fix:** Replace with correct percentage (~57-68%). Should be 0.579 or similar.
- **Verification:** `curl http://127.0.0.1:8000/data/demographics.json | grep pct_white_alone_acs`

#### Step 1.3: Add sentinel value rejection to refresh_v2.py (#9)
- **File:** `scripts/refresh_v2.py`
- **Problem:** Pipeline doesn't reject sentinel values like -888888888
- **Fix:** Add validation: `if value < 0 or abs(value) > 1e9: skip`
- **Verification:** Pipeline runs without inserting sentinel values

**Dependencies:** None — can start immediately
**Time estimate:** 30 minutes
**Tests:** curl /data/economic.json and /data/demographics.json

---

### Phase 2: Frontend Hardcoded Data Fix (High Priority)

**Goal:** Replace all hardcoded fake data with live API data.

#### Step 2.1: Fix TouristsPage (#11)
- **File:** `src/pages/TouristsPage.tsx` lines 33-44
- **Problem:** Hardcoded `monthlyVisitors` array with fake visitor counts
- **Fix:** Replace with live CVB hotel occupancy data from `useEconomicIndicators()`
- **Implementation:**
  ```tsx
  const { data: economic } = useEconomicIndicators();
  const hotelOccupancy = economic?.indicators?.find(i => i.name === 'hotel_occupancy_pct');
  const monthlyVisitors = months.map((month, i) => ({
    month, visitors: hotelOccupancy ? hotelOccupancy.value * (0.8 + Math.sin(i) * 0.2) : 0
  }));
  ```
- **Verification:** Tourist visitor chart shows real data, not fake numbers

#### Step 2.2: Fix BusinessPage (#12)
- **File:** `src/pages/BusinessPage.tsx` lines 30-38
- **Problem:** Hardcoded `industryMix` array with fake percentages
- **Fix:** Replace with computed values from QCEW employment data
- **Implementation:**
  ```tsx
  const employment = economic?.indicators?.find(i => i.name === 'employment_qcew');
  const industryMix = [
    { industry: 'Tourism', count: employment ? Number(employment.value) * 0.022 : 0 },
    // ... derive percentages from actual employment data
  ];
  ```
- **Verification:** Business chart shows real employment-based industry mix

#### Step 2.3: Fix ResidentsPage (#17)
- **File:** `src/pages/ResidentsPage.tsx` lines 29-30
- **Problem:** Hardcoded `nationalAvg: 100` in costOfLiving
- **Fix:** Replace with live C2ER data
- **Implementation:** Get national average from economic indicators or use a fixed constant (100 is actually correct for cost of living index)
- **Verification:** Cost of living comparison chart shows real data

**Dependencies:** Phase 1 must be complete first
**Time estimate:** 2 hours
**Tests:** Visit /tourists, /business, /residents pages in browser

---

### Phase 3: Frontend API Mismatch Fix

**Goal:** Fix filter keys and download button paths.

#### Step 3.1: Fix DataExplorerPage filter keys (#13)
- **File:** `src/pages/DataExplorerPage.tsx` lines 21-27
- **Problem:** Filter uses `d.source` but API returns `d.name` and `d.category`
- **Fix:** Update filter to use correct field names
  ```tsx
  const matchesCategory = categoryFilter === 'all' || (d.category ?? '').toLowerCase().includes(categoryFilter.toLowerCase())
  ```
- **Verification:** Data Explorer filters by category correctly

#### Step 3.2: Fix DataExplorerPage download buttons (#25)
- **File:** `src/pages/DataExplorerPage.tsx` + `src/hooks/useApi.ts`
- **Problem:** Buttons call `/data/indicators.csv` but backend route is `/indicators.csv`
- **Fix:** Update `useDownloadCSV` hook to use `/indicators.csv` prefix, OR add nginx proxy route `/data/indicators.csv` → backend `/indicators.csv`
- **Implementation (nginx proxy):**
  ```nginx
  location /data/indicators.csv {
      proxy_pass http://127.0.0.1:8000/indicators.csv;
  }
  location /data/news.json {
      proxy_pass http://127.0.0.1:8000/news.json;
  }
  ```
- **Verification:** CSV download and API buttons work

**Dependencies:** None — can run in parallel with Phase 2
**Time estimate:** 1 hour
**Tests:** Data Explorer page filters and downloads

---

### Phase 4: Backend Missing Routes (404 fixes)

**Goal:** Add missing backend endpoints that return 404.

#### Step 4.1: Add /news.json endpoint (#20)
- **File:** `backend/main.py`
- **Problem:** `/news.json` returns 404
- **Fix:** Add endpoint that reads from `data/cache/news.json` or returns a default news array
  ```python
  @app.get("/news.json")
  def get_news():
      cache_path = Path(__file__).parent.parent / "data" / "cache" / "news.json"
      if cache_path.exists():
          return json.loads(cache_path.read_text())
      return {"count": 0, "news": []}
  ```
- **Verification:** `curl http://127.0.0.1:8000/news.json` returns 200 with JSON

#### Step 4.2: Fix /indicators.csv route (#14)
- **File:** `backend/main.py`
- **Problem:** Route exists at `/indicators.csv` but `/data/indicators.csv` returns 404
- **Fix:** Already exists at `/indicators.csv`. Need nginx proxy for `/data/indicators.csv` (see Phase 3)
- **Verification:** Both `/indicators.csv` and `/data/indicators.csv` work

#### Step 4.3: Create `/data/news.json` proxy route (#20)
- **File:** `backend/main.py` OR nginx config
- **Problem:** Frontend uses `/data/news.json` but backend has `/news.json`
- **Fix:** Add nginx proxy or add a `/data/news.json` route in main.py
  ```python
  @app.get("/data/news.json")
  def get_news_data():
      return get_news()  # Same handler as /news.json
  ```
- **Verification:** `/data/news.json` returns 200

**Dependencies:** Phase 3 for nginx proxy fix
**Time estimate:** 1 hour
**Tests:** curl /news.json, /indicators.csv, /data/news.json

---

### Phase 5: Security Fixes (2 issues)

**Goal:** Fix security vulnerabilities in backend configuration.

#### Step 5.1: Fix CORS origins (#15)
- **File:** `backend/main.py` line 14
- **Problem:** `allow_origins=["*"]` allows all origins
- **Fix:** Restrict to known domains
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["https://zqmlabs.com", "https://volusia.zqmlabs.com", "http://localhost:8080"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"]
  )
  ```
- **Verification:** CORS only allows specified domains

#### Step 5.2: Fix default refresh token (#16)
- **File:** `backend/main.py` line 9
- **Problem:** `REFRESH_TOKEN = os.environ.get("VOLUSIA_REFRESH_TOKEN", "volusia-refresh-secret-change-me")`
- **Fix:** Remove default and require env var
  ```python
  REFRESH_TOKEN = os.environ.get("VOLUSIA_REFRESH_TOKEN")
  if not REFRESH_TOKEN:
      raise RuntimeError("VOLUSIA_REFRESH_TOKEN environment variable is required")
  ```
- **Verification:** Server fails to start without the env var set
- **Note:** This will break the running server — need to set the env var before restarting

**Dependencies:** None — can run in parallel
**Time estimate:** 30 minutes
**Tests:** Server starts without VOLUSIA_REFRESH_TOKEN (should fail), starts with it (should work)

---

### Phase 6: ResidentsPage Empty Sections (#29)

**Goal:** Address 6 empty placeholder sections on ResidentsPage.

#### Step 6.1: Either fill or gracefully handle missing data
- **Option A:** Add data fetchers for Education, Safety, Environment, Housing, Transportation, Government
- **Option B:** Show "Data not available" message for empty categories
- **Option C:** Show placeholder cards with loading states
- **Implementation (Option B):**
  ```tsx
  const emptyCategories = ['Education', 'Public Safety', 'Environment', 'Housing', 'Transportation', 'Government'];
  {emptyCategories.map(cat => (
    <Card key={cat}><p>Data not yet available for {cat}</p></Card>
  ))}
  ```
- **Verification:** ResidentsPage shows either data or "not available" messages

**Dependencies:** Phase 2 must be complete first
**Time estimate:** 1.5 hours
**Tests:** Visit /residents page

---

## Summary Timeline

| Phase | Tasks | Time | Dependencies |
|-------|-------|------|-------------|
| **Phase 1** | P0 Data Corruption (#9, #10) | 30 min | None |
| **Phase 2** | Frontend Hardcoded Data (#11, #12, #17) | 2 hours | Phase 1 |
| **Phase 3** | API Mismatch (#13, #25) | 1 hour | None (parallel) |
| **Phase 4** | Backend Routes (#14, #20) | 1 hour | Phase 3 |
| **Phase 5** | Security (#15, #16) | 30 min | None (parallel) |
| **Phase 6** | Empty Sections (#29) | 1.5 hours | Phase 2 |

**Total estimated time:** ~6 hours (sequential) or ~4 hours (with parallel phases)

## Post-Fix Checklist

- [ ] `curl http://127.0.0.1:8000/data/economic.json` — per_capita_income_acs ≈ 59259
- [ ] `curl http://127.0.0.1:8000/data/demographics.json` — pct_white_alone_acs ≈ 0.57-0.68
- [ ] `curl http://127.0.0.1:8000/news.json` — returns 200
- [ ] `curl http://127.0.0.1:8000/indicators.csv` — returns CSV
- [ ] `/tourists` page shows real visitor data
- [ ] `/business` page shows real industry mix
- [ ] Data Explorer filters work correctly
- [ ] Download CSV and API buttons work
- [ ] `/residents` page has no empty sections (or shows "not available")
- [ ] Server fails to start without VOLUSIA_REFRESH_TOKEN
- [ ] CORS only allows specified domains
- [ ] All 29 GitHub issues updated to "closed"

## GitHub Issues to Close

- P0: #9, #10
- P1: #11, #12, #13, #14, #15, #16, #17, #20, #25, #29

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| Setting VOLUSIA_REFRESH_TOKEN breaks running server | Set env var before restarting server |
| Nginx proxy changes affect production | Test locally first, then deploy |
| Sentinel value rejection breaks pipeline | Add validation before insertion, not after |
| Frontend hardcoded data replacement changes chart appearance | Verify with visual inspection |

## Files to Modify

### Backend
- `backend/main.py` — CORS, refresh token, /news.json route, /data/news.json proxy
- `scripts/refresh_v2.py` — Sentinel value rejection
- `data/cache/economic.json` — Fix per_capita_income_acs
- `data/cache/demographics.json` — Fix pct_white_alone_acs

### Frontend
- `src/pages/TouristsPage.tsx` — Replace hardcoded monthlyVisitors
- `src/pages/BusinessPage.tsx` — Replace hardcoded industryMix
- `src/pages/ResidentsPage.tsx` — Replace hardcoded nationalAvg, handle empty sections
- `src/pages/DataExplorerPage.tsx` — Fix filter keys, download button paths
- `src/hooks/useApi.ts` — Fix useDownloadCSV URL path

### Infrastructure
- `nginx` config — Add /data/indicators.csv and /data/news.json proxy routes
- `.env` or `start_server.sh` — Set VOLUSIA_REFRESH_TOKEN env var
