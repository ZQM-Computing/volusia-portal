# Project Volusia — Maintenance, Growth & Contribution Outline

> **Owner:** Alex Zelenski (zqmco)
> **Version:** 1.0
> **Date:** 2026-09-08
> **Classification:** Internal — Living Document
> **Board:** [GitHub Projects #7](https://github.com/users/ZQM-Computing/projects/7)

---

## 1. Project Overview

**Project Volusia** is an open-source public data portal and intelligence platform for Volusia County, Florida (FIPS 12127). It serves four constituencies — business owners, residents, tourists, and industry movers — with free, citable, machine-readable data from public sources.

| Attribute | Value |
|-----------|-------|
| **Repo** | `ZQM-Computing/volusia-portal` |
| **Live site** | `https://zqmlabs.com` (static site) |
| **API** | `http://127.0.0.1:8000` (FastAPI) |
| **Stack** | React 18 + Vite + TS + Tailwind + Nivo + Leaflet / FastAPI + SQLite |
| **License** | MIT |
| **Strategic window** | Q4 2026 – Full Year 2027 (sole focus) |

---

## 2. System Architecture

```
Frontend (React SPA) -> FastAPI :8000 -> SQLite volusia.db
                                  -> nginx :80 -> zqmlabs.com
                                  -> GitHub Pages :8089 -> gh-pages branch
```

### Key files

| Layer | File | Purpose |
|-------|------|---------|
| Frontend | `src/App.tsx` | Router, page structure |
| Frontend | `src/hooks/useApi.ts` | All API calls |
| Frontend | `src/pages/*.tsx` | 10 page components |
| Frontend | `src/types/index.ts` | TypeScript interfaces |
| Backend | `backend/main.py` | FastAPI app, all routes |
| Backend | `backend/gamification/` | Scoring engine, routes |
| Backend | `backend/data/volusia.db` | SQLite (80KB, 7 tables) |
| Pipeline | `scripts/refresh_v2.py` | Unified fetcher + DB sync |
| Pipeline | `scripts/scraper.py` | Legacy scraper |
| Data | `data/cache/*.json` | 28 cached datasets |
| Config | `.env.example` | Environment template |
| Config | `docker-compose.yml` | Docker deployment |
| Config | `nginx/` | nginx.conf with 13 security headers |

---

## 3. Current State Assessment

### What Works ✅

| Component | Status | Details |
|-----------|--------|---------|
| Backend API | ✅ Live | 26 indicators, 4 categories, 7 tables |
| Frontend build | ✅ Zero TS errors | P0 bugs fixed in commit faee0e2 |
| Data pipeline | ✅ Working | v6 with normalization, clean values |
| CI/CD | ✅ Green | 7/7 tests pass, GitHub Pages deploy |
| Gamification | ✅ Live | XP/levels, missions, leaderboard, pulse |
| Static site | ✅ zqmlabs.com | 200 OK, SEO headers, RSS feed |
| Contribution system | ✅ Live | 8 pathway templates, web + SMS |
| GitHub repo | ✅ Public | 13 topics, deprecation-bot PRs |
| P0 bug fixes | ✅ Merged | Math.random() removed, duplicate cards fixed |

### What's Broken 🔴

| Issue | Impact | Fix |
|-------|--------|-----|
| Docker Desktop STOPPED | Docker path unavailable | Use native uvicorn |
| cloudflared tunnel STOPPED | zqmlabs.com via tunnel down | `nssm start cloudflared` (admin) |
| 9 stub categories | Empty data (39-byte files) | Build fetchers |
| Ollama exposed to LAN | Security risk | Remove firewall rules, set OLLAMA_HOST |
| API keys in .env | Security risk | Move to GitHub secrets |

### What's Sparse ⚠️

| Category | File | Size | Notes |
|----------|------|------|-------|
| Housing | `zillow_zhvi.json` | 2.2KB | Partial data |
| Tourism | `tourism.json` | 1.3KB | Dec 2021 CVB data |
| Economic | `c2er` | cached | 2025Q1 only |
| Business | `volusia_business.json` | 221B | Sparse |
| GIS | `volusia_gis.json` | 295B | Sparse |

---

## 4. Maintenance Plan

### 4.1 Daily Operations

```bash
# Check backend health
curl http://127.0.0.1:8000/health

# Check static site
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8089/

# Refresh data
cd /c/Users/zqmco/Docker/volusia-portal
python scripts/refresh_v2.py

# Check indicator count
curl http://127.0.0.1:8000/indicators | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['count'])"
```

### 4.2 Weekly Maintenance

| Task | Command | Owner |
|------|---------|-------|
| Verify all cache files fresh | `ls -la data/cache/*.json` | zqmco |
| Check DB integrity | `sqlite3 data/volusia.db "PRAGMA integrity_check;"` | zqmco |
| Review open issues | `gh issue list --repo ZQM-Computing/volusia-portal` | zqmco |
| Merge dependabot PRs | `gh pr merge --auto` | zqmco |
| Update PROJECT_TRACKING.md | Edit and commit | zqmco |

### 4.3 Monthly Maintenance

| Task | Command | Owner |
|------|---------|-------|
| Run full test suite | `pytest tests/` | zqmco |
| Verify TS compilation | `npx tsc --noEmit` | zqmco |
| Rebuild frontend | `npm run build` | zqmco |
| Check GitHub Pages deploy | `curl https://volusia.zqmlabs.com` | zqmco |
| Backup database | `cp data/volusia.db data/backups/volusia-$(date +%Y%m%d).db` | zqmco |
| Review stale data | Check cache file mtimes | zqmco |

### 4.4 Quarterly Maintenance

| Task | Notes |
|------|-------|
| Charter review | Align with STRATEGIC_FOCUS_Q4_2026_2027.md |
| Data source re-verification | Re-test all 50+ sources |
| Stakeholder interview | 2 per group, 4 groups = 8 interviews |
| Project board review | Update PROJECT_TRACKING.md |
| API key rotation | Check .env, rotate if needed |
| Security audit | Check npm deps, Python deps |
| Infrastructure review | Docker, cloudflared, nginx config |

---

## 5. Growth Roadmap

### Phase 1: Foundation (Q4 2026 – Q2 2027) ✅ IN PROGRESS

| Milestone | Tasks | Status |
|-----------|-------|--------|
| **1A: Fix frontend bugs** | Replace Math.random(), fix filter keys, wire API | ✅ Done (commit faee0e2) |
| **1B: Fill data gaps** | Build fetchers for 9 stub categories | 🟡 In progress |
| **1C: Infrastructure** | Start Docker, restart cloudflared, reconcile ports | 🟡 Pending |
| **1D: Add API keys** | Register for Census, BLS, BEA, FRED keys | 🟡 Pending |
| **1E: Expand indicators** | Target 50+ across 10 categories | 🟡 In progress |
| **1F: Stakeholder interviews** | 8 interviews across 4 constituencies | 🟡 Planned |
| **1G: Contribution UI** | Build web form, integrate SMS gateway | 🟡 Planned |
| **1H: Documentation** | Update README, add CONTRIBUTING improvements | ✅ Mostly done |

### Phase 2: Access (Q2 2027 – Q4 2027)

| Milestone | Tasks | Status |
|-----------|-------|--------|
| **2A: Public portal v2.0** | Searchable, API-driven, mobile-first | ⏳ Planned |
| **2B: Business dashboards** | Free, plain-language, actionable | ⏳ Planned |
| **2C: Resident data access** | Community meetings, translated materials | ⏳ Planned |
| **2D: Tourist real-time APIs** | Conditions, availability, events | ⏳ Planned |
| **2E: Developer portal** | Documentation, SDKs, sandbox | ⏳ Planned |
| **2F: Quarterly briefings** | Public economic briefings | ⏳ Planned |
| **2G: Community input** | Web form + SMS + kiosks live | ⏳ Planned |

### Phase 3: Maturity (2028+)

| Milestone | Tasks |
|-----------|-------|
| **3A: AI insights** | Ollama-powered analysis of trends |
| **3B: Predictive models** | Economic forecasting, population projections |
| **3C: Open data API** | Public REST API with rate limiting |
| **3D: Mobile app** | Native or PWA for residents |
| **3E: Multi-county** | Expand to neighboring counties |
| **3F: Federation** | ZQM-MESH integration across nodes |

---

## 6. Contribution Guide

### 6.1 Three Pathways

| Pathway | Type | Entry Point |
|---------|------|-------------|
| **A — Data Source** | Add new data fetcher | `scripts/refresh_v2.py` |
| **B — Code/Feature** | Frontend or backend feature | PR to master |
| **C — Content/Gov** | Docs, governance, strategy | NAS + repo |

### 6.2 Adding a New Data Source (Pathway A)

```python
# 1. Add fetcher to scripts/refresh_v2.py
def fetch_new_source() -> Optional[dict]:
    """Fetch data from new source."""
    url = "https://example.com/api/data"
    data = http_get_json(url)
    if not data: return None
    return {"source": "Source Name", "value": ..., "category": "Category"}

# 2. Add to run_pipeline()
def run_pipeline():
    # ... existing fetchers ...
    result = fetch_new_source()
    if result:
        upsert_indicator(result['name'], result['value'], ...)
        export_json()

# 3. Add frontend hook in src/hooks/useApi.ts
export function useNewCategory() { return useApiData<any>('/new_category.json') }

# 4. Verify
curl http://127.0.0.1:8000/indicators?category=NewCategory
```

### 6.3 Adding a Frontend Feature (Pathway B)

```tsx
# 1. Create page in src/pages/NewPage.tsx
# 2. Add route in src/App.tsx
# 3. Add hook in src/hooks/useApi.ts if needed
# 4. Ensure npx tsc --noEmit passes
# 5. Ensure npm run build passes
# 6. Submit PR
```

### 6.4 Contribution Templates

Available at `CONTRIBUTION/templates/`:
- `ANALYSIS_SUBMISSION.md` — Data analysis submissions
- `COMMUNITY_INPUT.md` — Community feedback
- `DATA_SOURCE_SUBMISSION.md` — New data source proposals
- `DIRECT_CONTRIBUTION.md` — Direct code/feature contributions
- `MAP_SUBMISSION.md` — New map layers
- `SCHOOL_PROJECT_SUBMISSION.md` — Academic contributions
- `SOCIAL_MEDIA_INPUT.md` — Social media engagement
- `TOOL_SUBMISSION.md` — New tools/utilities

### 6.5 Code Standards

| Standard | Rule |
|----------|------|
| TypeScript | `npx tsc --noEmit` must pass with zero errors |
| Tests | `pytest tests/` must pass (7/7) |
| Build | `npm run build` must succeed |
| Git | Conventional commits (`feat:`, `fix:`, `chore:`) |
| API | All fetchers use `http_get_json()` or `fetch_url()` |
| Cache | All data cached in `data/cache/` with 24h TTL |
| DB | SQLite with WAL + busy_timeout + foreign_keys on every connection |
| Security | `/refresh` requires `?secret=` HMAC auth |
| Headers | nginx serves 13 security headers |

---

## 7. Data Strategy

### 7.1 Target Categories (11 total)

| # | Category | Status | Indicators | Gap |
|---|----------|--------|------------|-----|
| 1 | Demographics | ✅ Live | population, median_age, pct_over_65, pct_bachelors | None |
| 2 | Economic | ✅ Live | income, poverty, unemployment, CPI | Per-capita income sentinel |
| 3 | Climate | ✅ Live | avg_max_temp, avg_min_temp, total_precip | Historical depth |
| 4 | Tourism | ⚠️ Stale | ADR, occupancy, RevPAR | Dec 2021 only |
| 5 | Housing | ❌ Stub | — | Needs Zillow fetcher |
| 6 | Business | ❌ Stub | — | Needs VolusiaBusiness.org fetcher |
| 7 | Education | ❌ Stub | — | Needs FL DOE / NCES fetcher |
| 8 | Government | ❌ Stub | — | Needs county data fetcher |
| 9 | Health | ❌ Stub | — | Needs CDC PLACES / FL CHARTS fetcher |
| 10 | Safety | ❌ Stub | — | Needs FDLE / Sheriff fetcher |
| 11 | Transportation | ❌ Stub | — | Needs FDOT / NTD fetcher |

### 7.2 Source Tier System

| Tier | Criteria | Examples |
|------|----------|----------|
| **Tier 1** | Free, no key, immediate | Census PEP, Open-Meteo, NOAA NCEI |
| **Tier 2** | Free, key required | Census ACS, BLS LAUS, BEA CAINC1, FRED, FBI UCR |
| **Tier 3** | Free, scrape/download | SAM.gov, USASpending, FHFA HPI, EPA AQS |
| **Tier 4** | Paid / future | AirDNA, ATTOM, STR |

### 7.3 Data Quality Framework

```
quality_score = f(authority, vintage_freshness, metadata_completeness, cross_reference)
  authority = 80-100 (gov source), 60-79 (commercial), 40-59 (community)
  vintage_freshness = 100 (≤90 days), decreasing over time
  metadata_completeness = source_url, vintage, fetchedAt, description present
  cross_reference = agreement with independent sources

quality_tier = Verified (90+) | Reviewed (70-89) | Pending (50-69) | Flagged (<50)
```

---

## 8. Infrastructure Plan

### 8.1 Current Services

| Service | Port | Status | Notes |
|---------|------|--------|-------|
| nginx | :80 | ✅ | Static site + 13 security headers |
| FastAPI | :8000 | ✅ | Native uvicorn (not Docker) |
| VolusiaWeb | :8089 | ✅ | Static site via nginx |
| Docker Desktop | — | ❌ | STOPPED — app runs natively |
| cloudflared | — | ❌ | STOPPED — needs admin start |
| Ollama | :11434 | ⚠️ | Exposed to LAN, no auth |

### 8.2 Docker Compose

```yaml
frontend: 8080:80  # React SPA
backend: 8000:8000  # FastAPI
searxng: 8081:8080  # Optional search
```

**Port conflict:** Traefik routes zqmlabs.com → :8089 (static site). Running `docker compose up` will conflict on :8080/:8089. Reconcile before bringing Docker up.

### 8.3 GitHub Pages Deploy

```yaml
# .github/workflows/deploy.yml
# Pushes to gh-pages branch with cname: volusia.zqmlabs.com
# Triggered on push to master or workflow_dispatch
```

### 8.4 Infrastructure To-Dos

| Task | Priority | Fix |
|------|----------|-----|
| Start cloudflared tunnel | HIGH | `nssm start cloudflared` (admin) |
| Start Docker Desktop | MEDIUM | Enable Docker Desktop, reconcile ports |
| Secure Ollama | HIGH | Remove 8 firewall rules, set `OLLAMA_HOST=127.0.0.1` |
| Rotate API keys | MEDIUM | Move keys from .env to GitHub secrets |
| Add healthchecks to docker-compose | MEDIUM | Add healthcheck blocks to services |
| Set up cron refresh | HIGH | `volusia-refresh-hourly` created 2026-09-07 |
| Backup database | LOW | Add to monthly maintenance |

---

## 9. Gamification System

### 9.1 XP/Level Structure

| Level | XP | Description |
|-------|-----|-------------|
| Newcomer | 0+ | First contribution |
| Explorer | 100+ | Active contributor |
| Analyst | 500+ | Reliable data source |
| Steward | 1500+ | Consistent quality |
| Architect | 5000+ | Top contributor |

### 9.2 Mission Catalog

| Mission | XP | Trigger |
|---------|-----|---------|
| First Spark | 50 | First submission |
| Streak 7 | 100 | 7-day contribution streak |
| Streak 30 | 250 | 30-day contribution streak |
| Verified Contributor | 200 | Reach Verified quality tier |
| Data Steward | 300 | 5+ accepted submissions |
| Sector Pioneer | 400 | Submit in all 4 constituencies |
| Community Voice | 150 | 10+ total contributions |

### 9.3 Quality Framework

```python
compute_quality_score(submission, existing_submissions)
  → returns {quality_score: int (0-100), quality_tier: str}
```

Scoring factors: source authority (60-100), vintage freshness, metadata completeness, cross-reference agreement.

### 9.4 Gamification Endpoints

- `POST /gamification/contribute` — Submit a contribution
- `GET /gamification/quality` — Get quality scores
- `GET /gamification/reputation/{id}` — Get contributor reputation
- `GET /gamification/leaderboard` — Get leaderboard
- `GET /gamification/pulse` — Get constituency pulse
- `GET /gamification/profile/{id}` — Get contributor profile
- `POST /gamification/visit/{user_id}` — Track page visit

---

## 10. Governance & Decision Framework

### 10.1 Team Roles

| Role | Status | Scope |
|------|--------|-------|
| Executive Sponsor | Alex Zelenski | Strategic direction, resource allocation |
| Technical Lead | Open | Architecture, tooling, deployment |
| Data Lead | Open | Sources, quality, indicator definitions |
| Research Lead | Open | Methodology, interviews, reports |
| Ops/Comms Lead | Open | Stakeholder comms, documentation |

### 10.2 Decision Tiers

| Tier | Who Decides | Examples |
|------|-------------|----------|
| Tier 1 — Autonomous | Lead within scope | Function names, library versions |
| Tier 2 — Informed | Lead decides | New source meeting tier standard |
| Tier 3 — Consensus | Relevant leads | Methodology changes, stakeholder commitments |
| Tier 4 — Executive | Alex Zelenski | Strategic direction, phase transitions |

### 10.3 Meeting Cadence

| Frequency | Meeting | Purpose |
|-----------|---------|---------|
| Weekly | Operational sync | Progress, blockers, assignments |
| Monthly | Stakeholder review | Findings, feedback, updates |
| Quarterly | Formal review (Dec 2) | Charter alignment, milestone check |
| Annual | Strategic planning | Next year's focus |

---

## 11. Automation

### 11.1 Cron Jobs

| Job | Schedule | Script | Purpose |
|-----|----------|--------|---------|
| `volusia-refresh-hourly` | `0 * * * *` | `scripts/refresh_v2.py` | Refresh data every hour |
| Old daily `volusia-data-refresh` | Removed | — | Replaced by hourly |

### 11.2 CI Pipeline

```yaml
# .github/workflows/ci.yml
# On push/PR to master:
#   1. npm ci
#   2. npm run build
#   3. npx tsc --noEmit  (zero errors)
```

### 11.3 Deploy Pipeline

```yaml
# .github/workflows/deploy.yml
# On push to master or workflow_dispatch:
#   1. npm ci, npm run build
#   2. Deploy to gh-pages branch
#   3. CNAME: volusia.zqmlabs.com
```

### 11.4 Watchdog

```python
# scripts/watchdog_monitoring.py
# Monitors data freshness per-source thresholds
# Alerts when cache files exceed TTL
```

---

## 12. Security

### 12.1 Current Security Posture

| Control | Status |
|---------|--------|
| nginx security headers | ✅ 13 headers (HSTS, CSP, Permissions-Policy, etc.) |
| `/refresh` HMAC auth | ✅ `?secret=` validated with `hmac.compare_digest` |
| CORS | ✅ `allow_origins=["*"]` (consider restricting) |
| API keys | ⚠️ In `.env` — move to GitHub secrets |
| Ollama | ⚠️ Exposed on `0.0.0.0:11434` — needs auth |
| `.env` in .gitignore | ✅ Not committed |
| `data/volusia.db` in .gitignore | ✅ Not committed |

### 12.2 Security To-Dos

| Task | Priority |
|------|----------|
| Move API keys to GitHub secrets | HIGH |
| Secure Ollama (remove firewall rules, set OLLAMA_HOST) | HIGH |
| Restrict CORS to specific origins | MEDIUM |
| Add rate limiting to API endpoints | MEDIUM |
| Rotate API keys (currently in .env) | MEDIUM |

---

## 13. Documentation Map

### 13.1 Public-Facing (on GitHub / zqmlabs.com)

| Doc | Location | Purpose |
|-----|----------|---------|
| README.md | Repo root | Project overview, quick start |
| CONTRIBUTING.md | Repo root | How to contribute |
| PROJECT_TRACKING.md | Repo root | Living project board |
| PROJECT_OUTLINE.md | Repo root | Maintenance/growth/contribution |
| API.md | Repo root | API documentation |
| SECURITY.md | Repo root | Security policy |
| DEPLOY.md | Repo root | Deployment guide |
| METHODOLOGY.md | Repo root | Research methodology |
| index.html | Repo root / nginx | Static site landing page |
| sitemap.xml | Repo root | SEO |
| rss.xml | Repo root | Data updates feed |

### 13.2 Internal (on NAS only)

| Doc | NAS Location | Purpose |
|-----|-------------|---------|
| STRATEGIC_FOCUS_Q4_2026_2027.md | `14_Projects/Active/Project-Volusia/` | Sole focus declaration |
| PROJECT_VOLUSIA_GOV.md | `14_Projects/Active/Project-Volusia/` | Governance charter |
| Q4_2026_EXECUTION_PLAN.md | `14_Projects/Active/Project-Volusia/` | Operational plan |
| Q4_2026_DELIVERY_STATUS.md | `14_Projects/Active/Project-Volusia/` | Delivery checklist |
| GUIDING_PRINCIPLES_VOLUSIA_COUNTY.md | `14_Projects/Active/Project-Volusia/` | Community charter |
| TIMELINE_AND_ROADMAP.md | `14_Projects/Active/Project-Volusia/` | Historical + roadmap |
| PRIORITY_TRADEOFFS.md | `14_Projects/Active/Project-Volusia/` | Tradeoff decisions |
| RECON_REPORT_V3.md | Repo root | 50+ data source survey |
| PUBLIC_DATA_SOURCE_RECON.md | Repo root | Full reconnaissance |
| DATA_ASSET_AUDIT_VOLUSIA.md | Repo root | Data asset audit |
| CONTRIBUTION_LOG.md | Repo root | Contribution history |

---

## 14. Key Metrics & Success Indicators

### 14.1 Data Coverage Targets

| Metric | Current | Target |
|--------|---------|--------|
| Live indicators | 26 | 50+ |
| Data categories | 4 | 11 |
| Data sources | 6 verified | 50+ surveyed |
| Cache files | 28 | 50+ |
| Map layers | 18 | 25+ |
| Gamification users | 3 | 100+ |

### 14.2 Technical Health Targets

| Metric | Current | Target |
|--------|---------|--------|
| TypeScript errors | 0 | 0 |
| Test pass rate | 7/7 (100%) | 100% |
| Build success | ✅ | ✅ |
| API uptime | ~99% | ~99.9% |
| Data freshness | 24h TTL | Per-source cadence |
| Security headers | 13 | 13+ |

### 14.3 Community Targets

| Metric | Current | Target |
|--------|---------|--------|
| GitHub stars | 0 | 50+ |
| Open issues | 7 | <10 |
| Contributors | 1 (zqmco) | 5+ |
| Stakeholder interviews | 0 | 8 (2 per group) |
| Contribution submissions | 3 | 20+ |

---

## 15. Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Docker Desktop continues failing | High | Medium | Use native uvicorn, document it |
| API keys expire or revoked | Medium | High | Monitor, rotate, use GitHub secrets |
| Data sources restructure or go behind paywall | High | Medium | RECON_REPORT_V3.md tracks alternatives |
| Frontend bugs remain unfixed | Medium | High | Issue #7 is P0 — already fixed |
| cloudflared tunnel stays stopped | Medium | Medium | nginx serves directly on :80 |
| Ollama security exposure | Medium | High | Remove firewall rules, set OLLAMA_HOST |
| Contributor burnout | Low | Medium | Automated pipeline reduces manual work |
| GitHub token scopes lost | Low | Medium | Refresh auth, update `gh` config |
| NAS (ZQM-GARDEN-03) goes offline | Low | High | Git repo is the source of truth |
| SQLite lock under concurrent load | Low | Medium | WAL + busy_timeout on every connection |

---

## 16. Quick Reference

### Start the stack
```bash
# Backend (native Python — no Docker needed)
cd /c/Users/zqmco/Docker/volusia-portal
uvicorn backend.main:app --host 127.0.0.1 --port 8000

# Frontend
cd /c/Users/zqmco/Docker/volusia-portal
npm run dev  # http://localhost:5173
```

### Check status
```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/indicators
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8089/
curl -s -o /dev/null -w '%{http_code}' https://zqmlabs.com/
```

### Refresh data
```bash
cd /c/Users/zqmco/Docker/volusia-portal
python scripts/refresh_v2.py
curl http://127.0.0.1:8000/refresh?secret=volusia-refresh-secret-change-me
```

### Run tests
```bash
cd /c/Users/zqmco/Docker/volusia-portal
pytest tests/
npx tsc --noEmit
npm run build
```

### GitHub operations
```bash
gh issue list --repo ZQM-Computing/volusia-portal
gh issue create --title "[FEATURE]" --body "..." --repo ZQM-Computing/volusia-portal
gh pr list --repo ZQM-Computing/volusia-portal
```

---

*Last updated: 2026-09-08*
*Next review: 2026-12-02 (quarterly charter review)*
*Owner: Alex Zelenski, zqmco*
*Board: [GitHub Projects #7](https://github.com/users/ZQM-Computing/projects/7)*
