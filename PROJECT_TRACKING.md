# Project Volusia — GitHub Project Tracking

> **Owner:** Alex Zelenski (zqmco)
> **Created:** 2026-09-08
> **Repo:** [ZQM-Computing/volusia-portal](https://github.com/ZQM-Computing/volusia-portal)
> **Live:** [zqmlabs.com](https://zqmlabs.com) | **API:** [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Project Status

| Metric | Value |
|--------|-------|
| **Live indicators** | 29+ (across 4 categories) |
| **DB size** | 80KB SQLite (volusia.db) |
| **Frontend build** | ✅ 0 TypeScript errors |
| **Backend** | ✅ FastAPI :8000 healthy |
| **Static site** | ✅ nginx :8089 → zqmlabs.com |
| **Docker Desktop** | ❌ STOPPED (app runs natively via uvicorn) |
| **cloudflared tunnel** | ❌ STOPPED (NSSM needs admin start) |
| **Open GitHub issues** | 7 |
| **GitHub Projects board** | ⏳ Pending `project` scope on token |

---

## Milestones

### Milestone 1: Foundation Complete (2026-09-03) ✅
- Pipeline end-to-end verified (6/6 data sources)
- 13 indicators loaded → now 29+ via v5/v6 pipeline improvements
- All governance docs published (PROJECT_VOLUSIA_GOV, METHODOLOGY, PRIORITY_TRADEOFFS, etc.)
- Contribution system operational (8 pathways)
- CI green (7/7 tests pass)
- GitHub Pages deploy working (gh-pages branch)

### Milestone 2: Data Enrichment (In Progress)
- Target: Fill 9 stub categories (business, education, government, health, housing, safety, transportation)
- Target: 50+ indicators across 10 categories
- Target: Replace all `Math.random()` fake data with real API calls
- Remote has v5/v6 pipeline improvements already merged (c4dd8c5, 50e63b3, 42aac1b)

### Milestone 3: Frontend Hardening (In Progress)
- Fix DataExplorerPage `Math.random()` charts (CRITICAL — fake data shown as real)
- Fix broken filter keys in DataExplorerPage
- Fix HomePage chart key mismatches (`median_income` → `median_household_income_acs`)
- Fix ResidentsPage duplicate StatCard and hardcoded arrays
- Fix MapsPage hardcoded county polygon
- Remove unused `useIndicator` hooks

### Milestone 4: Infrastructure (Pending)
- Start Docker Desktop / reconcile port conflicts (:8080/:8000 vs :8089)
- Restart cloudflared tunnel (`nssm start cloudflared` as admin)
- Get `project` scope on GitHub token for Projects board (`gh auth refresh -s project,read:project`)
- Deploy v2.0 to zqmlabs.com with real content

### Milestone 5: Phase 1 Complete (Target: 2027-Q2)
- All 50+ data sources operational
- All 7 portal routes fully data-connected
- Gamification system live (scoring, quality tiers, reputation, leaderboard)
- Public API with documentation
- Stakeholder interviews completed

---

## Open Issues (GitHub)

| # | Title | Status | Priority |
|---|-------|--------|----------|
| 7 | [P0] Fix critical frontend bugs from 2026-09-08 audit | 🔴 OPEN | **P0 — CRITICAL** |
| 6 | Audit: Full Page-by-Page Enhancement Audit (2026-09-08) | 🔴 OPEN | **P0 — CRITICAL** |
| 5 | chore: bump @nivo/geo 0.87→0.99 | 🟡 OPEN | Low |
| 4 | build: bump postcss 8.5.26→8.5.28 | 🟡 OPEN | Low |
| 3 | chore: bump @nivo/line 0.87→0.99 | 🟡 OPEN | Low |
| 2 | chore: bump react-dom + @types/react-dom | 🟡 OPEN | Low |
| 1 | build: bump tailwindcss 3.4.19→4.3.3 | 🟡 OPEN | Low |

**Issue #7 sub-tasks (CRITICAL):**
- [ ] Fix DataExplorerPage: Replace `Math.random()` with real API data
- [ ] Fix DataExplorerPage: Correct filter keys to match API response structure
- [ ] Fix DataExplorerPage: Wire `useIndicator('unemployment_rate_acs')` and `useIndicator('median_household_income_acs')`
- [ ] Fix DataExplorerPage: Wire Dataset Download CSV / API buttons to handlers
- [ ] Fix HomePage: Chart filter keys to match API indicator names
- [ ] Fix HomePage: Map preview uses real map-layer counts
- [ ] Fix ResidentsPage: Remove duplicate pctBachelor StatCard
- [ ] Fix ResidentsPage: Wire costOfLiving and incomeTrend to API
- [ ] Fix MapsPage: Replace hardcoded county polygon with real GeoJSON
- [ ] Add missing dataset filter/status values to API response

---

## Data Source Status

| Category | Source | Status | Records |
|----------|--------|--------|---------|
| **Climate** | NOAA NCEI Daily Summaries | ✅ LIVE | 366 days |
| **Demographics** | Census ACS 5-Year DP05 | ✅ LIVE | population, median_age, pct_over_65, pct_bachelors |
| **Demographics** | Census PEP | ✅ LIVE | 2022, 2023, 2024 |
| **Economic** | BLS QCEW | ✅ LIVE | establishments, employment, avg_weekly_wage |
| **Economic** | BLS LAUS | ✅ LIVE | unemployment_rate, labor_force, unemployed |
| **Economic** | BEA Regional | ✅ LIVE | per_capita_income, personal_income_total, population |
| **Economic** | Census ACS DP03 | ✅ LIVE | median_household_income, poverty_rate, unemployment_rate |
| **Tourism** | Volusia County CVB | ⚠️ STALE | Dec 2021 data |
| **Economic** | C2ER Cost of Living | ⚠️ STALE | 2025Q1 cached |
| **Housing** | Zillow ZHVI | ⚠️ SPARSE | 2.2KB, partial |
| **Business** | Volusia Business | ❌ STUB | 39 bytes |
| **Education** | — | ❌ STUB | 39 bytes |
| **Government** | — | ❌ STUB | 39 bytes |
| **Health** | — | ❌ STUB | 84 bytes |
| **Housing** | — | ❌ STUB | 39 bytes |
| **Safety** | — | ❌ STUB | 39 bytes |
| **Transportation** | — | ❌ STUB | 39 bytes |

**Stub categories needing new fetchers:** business, education, government, health, housing, safety, transportation

---

## Infrastructure Issues

| Issue | Status | Fix |
|-------|--------|-----|
| Docker Desktop STOPPED | ❌ | Start Docker Desktop or use native uvicorn |
| cloudflared tunnel STOPPED | ❌ | `nssm start cloudflared` (admin) |
| Ollama :11434 exposed to LAN | ⚠️ | Remove firewall rules, set `OLLAMA_HOST=127.0.0.1` |
| GitHub token missing `project` scope | ⚠️ | `gh auth refresh -s project,read:project` (interactive) |
| API keys in working copy (.env) | ⚠️ | Rotate keys, use `.env.example` only |
| Port conflict (:8080/:8000 vs :8089) | ⚠️ | Reconcile Traefik config |
| Frontend `dist/` potentially stale | ⚠️ | Rebuild after frontend fixes |

---

## Workflow Status

| Workflow | File | Status |
|----------|------|--------|
| CI | `.github/workflows/ci.yml` | ✅ Working (build + tsc --noEmit) |
| Deploy | `.github/workflows/deploy.yml` | ✅ Working (GitHub Pages → gh-pages, cname: volusia.zqmlabs.com) |

---

## Contributing

### Quick Start
```bash
# Clone
git clone https://github.com/ZQM-Computing/volusia-portal.git
cd volusia-portal

# Backend (native Python — Docker Desktop is unreliable)
python scripts/refresh_v2.py  # populate DB
uvicorn backend.main:app --host 127.0.0.1 --port 8000

# Frontend
npm install
npm run dev  # http://localhost:5173
npm run build # zero TS errors required
```

### Adding a New Data Source
1. Add fetcher function to `scripts/refresh_v2.py`
2. Add cache file to `data/cache/{name}.json`
3. Upsert indicators to `data/volusia.db`
4. Update `data/cache/indicators.json`
5. Add frontend hook in `src/hooks/useApi.ts` if needed
6. Verify with `curl http://127.0.0.1:8000/indicators?category={cat}`

### Code Quality
- `npx tsc --noEmit` must pass with zero errors
- `npm test` must pass (7/7)
- PRs must pass CI (`npx tsc --noEmit` + `npm run build`)

### Issue Labels
- `bug` — Frontend/backend defects
- `enhancement` — New features, data sources
- `critical` — P0 bugs (fake data, broken pages)
- `infra` — Docker, cloudflared, nginx, networking
- `data` — Data pipeline, fetchers, cache issues

---

## Key Documents

| Document | Location |
|----------|----------|
| Strategic Focus | [NAS](http://zqm-garden-03/14_Projects/Active/Project-Volusia/STRATEGIC_FOCUS_Q4_2026_2027.md) |
| Governance | [NAS](http://zqm-garden-03/14_Projects/Active/Project-Volusia/PROJECT_VOLUSIA_GOV.md) |
| Execution Plan | [NAS](http://zqm-garden-03/14_Projects/Active/Project-Volusia/Q4_2026_EXECUTION_PLAN.md) |
| Delivery Status | [NAS](http://zqm-garden-03/14_Projects/Active/Project-Volusia/Q4_2026_DELIVERY_STATUS.md) |
| Data Sources | [RECON_REPORT_V3.md](RECON_REPORT_V3.md) |
| Methodology | [METHODOLOGY.md](METHODOLOGY.md) |
| Guiding Principles | [GUIDING_PRINCIPLES_VOLUSIA_COUNTY.md](GUIDING_PRINCIPLES_VOLUSIA_COUNTY.md) |
| Contributing | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Build Report | [BUILD_REPORT.md](BUILD_REPORT.md) |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-09-08 | Created PROJECT_TRACKING.md, issue #7 (critical bugs) | zqmco |
| 2026-09-08 | Remote merged v5/v6 pipeline improvements (c4dd8c5, 50e63b3, 42aac1b) | zqmco |
| 2026-09-07 | Frontend overhaul commit `2c346f0` — dark mode, mobile nav, error boundaries | zqmco |
| 2026-09-07 | Fix /diagnostics + GET /refresh auth `b819fd4` | zqmco |
| 2026-09-07 | HMAC auth on /refresh, WAL PRAGMAs, /pulse.json route | zqmco |
| 2026-09-07 | 29 indicators live, 18 map layers, 10 datasets | zqmco |
| 2026-09-06 | Full page-by-page audit (issue #6 created) | zqmco |
| 2026-09-03 | Repo created, pipeline working, 6/6 data sources | zqmco |
| 2026-09-02 | Strategic focus declaration, governance charter | zqmco |

---

*Last updated: 2026-09-08*
*Next review: 2026-12-02 (quarterly charter review)*
*Next milestone: Milestone 2 (Data Enrichment) / Milestone 3 (Frontend Hardening)*
