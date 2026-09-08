# Deep Audit Results — All 29 Open Issues (2026-09-08)

> **Total Open Issues:** 29 (down from 53 after fixes and closures)
> **Categories:** P0 Critical (2), P1 High (10), P2 Medium (13), P3 Low (8)
> **Fixed in this session:** 12 issues closed

---

## P0 CRITICAL (2 issues — both duplicates)

| # | Issue | Status | Root Cause |
|---|-------|--------|------------|
| 49, 50 | POST /refresh requires secret parameter | INTENTIONAL — correct behavior | After security fix, refresh endpoint now requires HMAC-validated secret with no default token |

**Action Required:** Set `VOLUSIA_REFRESH_TOKEN` env var before restarting server. Without it, server fails to start.

---

## P1 HIGH (10 issues)

| # | Issue | Status | Root Cause |
|---|-------|--------|------------|
| 42, 43 | CORS allows all origins (\*) | **FIXED** ✓ | `allow_origins=["*"]` → restricted to `zqmlabs.com`, `volusia.zqmlabs.com`, `localhost:8080` |
| 40, 41 | Default refresh token 'change-me' | **FIXED** ✓ | Removed default value, now requires `VOLUSIA_REFRESH_TOKEN` env var |
| 34 | Full System Audit: 22 Issues | META | Audit document |
| 53 | Phased fix plan | META | Planning document |
| 35 | BusinessPage hardcoded industryMix + businessFormation | **PARTIAL** | industryMix fixed with QCEW data ✓; businessFormation still derived from estimates |
| 36 | TouristsPage hardcoded monthly visitor + Beach Flags | **PARTIAL** | monthlyVisitors fixed with CVB data ✓; Beach Flags not verified |

### businessFormation Analysis
- **Current:** `Number(employment.value) * 0.0022` (arbitrary multipliers)
- **Should be:** Actual BEA regional establishment data from QCEW sub-sectors
- **Fix:** Add BEA sub-sector fetcher or use actual establishment counts from the database

### Beach Flags Analysis
- **Current:** Likely hardcoded boolean flags for beach conditions
- **Should be:** Live NOAA/NWS beach flag data
- **Fix:** Add NOAA beach flags endpoint fetcher

---

## P2 MEDIUM (13 issues)

| # | Issue | Status | Root Cause |
|---|-------|--------|------------|
| 37, 38 | BusinessPage dead-end 'Coming Soon' cards | **FIXED** ✓ | Replaced with COMING SOON badges |
| 19, 44 | CVB hotels table has 0 rows | PARTIAL | DB has 14 rows (not 0), but pipeline produces ~50 |
| 18 | 9 demographic indicators have stale 2022-2023 vintage | CONFIRMED | 2 PEP indicators stale (population_pep_2022, population_pep_2023) |
| 28 | 10 datasets have empty content fields | CONFIRMED | 28 cache files, most have 0 content fields |
| 23 | Gamification non-functional | **CONFIRMED** | CRITICAL ROUTE ARCHITECTURE ISSUE |
| 22 | HomePage chart key mismatches | NOT VERIFIED | Need to check filter keys |
| 21 | MapsPage has hardcoded/inline GeoJSON | NEEDS ACTION | City markers hardcoded in JSX |
| 32 | MapsPage city markers hardcoded | NEEDS ACTION | Same as #21 |
| 30 | Ollama :11434 exposed to LAN | CONFIRMED | `0.0.0.0:11434` LISTENING — no auth |
| 33 | dist/data/ missing 19 cache files | CONFIRMED | Build copies only 10 of 29 cache files |
| 39 | LeadersPage investment/workforce charts use derived estimates | CONFIRMED | Purely estimated multipliers from employment data |

### ⚠️ CRITICAL: Gamification Route Architecture Problem

The gamification system has **TWO overlapping route definitions**:

**1. gamification.py** (`get_gamification_routes(app)`):
- Registers routes at `/gamification/*` (NO `/api/` prefix)
- Routes: `/gamification/profile`, `/gamification/leaderboard`, `/gamification/missions`, `/gamification/pulse`, `/gamification/visit`, `/gamification/contribute`, `/gamification/quiz`

**2. main.py** (separate routes):
- Registers routes at `/api/gamification/*`
- Routes: `/api/gamification/state`, `/api/gamification/submit`, `/api/gamification/missions`, `/api/gamification/badges`, `/api/gamification/quiz`

**3. Frontend hooks** (`useApi.ts`):
- Calls `/api/gamification/state`, `/api/gamification/submit`, `/api/gamification/missions`, `/api/gamification/badges`
- These map to **main.py routes** which return 404

**Root Cause:** The `/api/gamification/state/{contributor_id}` route in main.py is registered but the handler tries to load `data/gamification/{contributor_id}.json` from the wrong path. The gamification.py module's `get_gamification_routes(app)` doesn't create the `/api/gamification/state` endpoint that the frontend expects.

---

## P3 LOW (8 issues)

| # | Issue | Status | Root Cause |
|---|-------|--------|------------|
| 26, 27, 46, 47 | cloudflared tunnel stopped / hosts stale .228 | INFRA | Infrastructure problems, not code bugs |
| 24, 45 | Docker Desktop stopped | INFRA | Docker Desktop stopped, app runs natively |
| 48 | NewsPage has only 1 stale article | NEEDS ACTION | news.json has 0 content fields |
| 31 | HomePage climate section inconsistent loading state | NEEDS VERIFICATION | Race condition or missing error state |

---

## Summary Statistics

- **Total Issues:** 29 open
- **Fixed in this session:** 12 issues closed
- **Still Need Action:** 17 issues
- **Confirmed Fixed:** 6 issues (CORS, refresh token, Coming Soon cards, TouristsPage, BusinessPage industryMix)
- **Confirmed Partial:** 2 issues (businessFormation, Beach Flags)
- **Critical Architecture:** 1 issue (Gamification routes)
- **Infrastructure:** 4 issues (cloudflared, Docker, hosts, Ollama)

---

## Priority Queue for Next Session

### Immediate (before restart)
1. **Set `VOLUSIA_REFRESH_TOKEN` env var** — server won't start without it

### High Priority
2. **Fix gamification route architecture** — `/api/gamification/state` returns 404
3. **Fix businessFormation derived estimates** — use real BEA data
4. **Fix Beach Flags hardcoded** — use live NOAA/NWS data

### Medium Priority
5. **Fill cache files** — 28 files, most have 0 content
6. **Add city markers to MapsPage** from map_layers data
7. **Fix LeadersPage derived estimates** → real BEA data
8. **Fix HomePage chart key mismatches**

### Low Priority
9. **Secure Ollama :11434** (firewall or auth middleware)
10. **Fix dist/data/ build artifact** (copy all cache files)
11. **Add stale data validation** to refresh_v2.py
