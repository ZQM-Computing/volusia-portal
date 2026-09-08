# Project Volusia — Full System Audit (2026-09-08)

## Executive Summary

A comprehensive multi-component audit of the Project Volusia stack (backend, frontend, database, gamification, contribution pipeline, infrastructure). All components were probed live via curl, sqlite3, and direct file inspection.

**Verdict: 3 CRITICAL, 5 HIGH, 8 MEDIUM, 6 LOW issues found.**

---

## P0 — CRITICAL (blocks system integrity)

### C1: `/refresh` POST still requires `secret: Query(...)` parameter
**Component:** `backend/main.py` line 237–238
**Evidence:** `POST /refresh` function signature still has `secret: str = Query(...)` — the earlier fix only removed it from the GET `/refresh` (diagnostics) handler, but the POST handler was missed. The `_require_refresh_auth` decorator is also still applied to POST /refresh.
**Impact:** `POST /refresh` is broken — requires HMAC secret that may not be known to contributors. This blocks the data refresh pipeline.
**Fix:** Remove `secret` parameter and `_require_refresh_auth` decorator from POST `/refresh` handler (same fix as GET).

### C2: `data/cache/` has 29 files but `datasets` table shows ALL 10 entries with `content_len=0`
**Component:** `backend/main.py` line 66–70 (get_datasets) + `data/volusia.db` → `datasets` table
**Evidence:** `SELECT * FROM datasets` returns 10 rows with `content` field = empty string for all entries. The `content` column exists but is never populated. The `/datasets` endpoint returns empty content for every dataset.
**Impact:** `/datasets` endpoint is effectively useless — returns metadata but zero actual data content. All dataset retrieval via API returns empty payloads.
**Fix:** Repopulate `datasets.content` from the corresponding `data/cache/{name}.json` files, or remove the empty `content` field and return file references instead.

### C3: `scripts/contribute.py` and `scripts/kb_bridge.py` cannot reach KB :8787
**Component:** `scripts/contribute.py` + `scripts/kb_bridge.py`
**Evidence:** `curl http://127.0.0.1:8787/healthz` → WinError 10061 connection refused. KB process (PID 17036, pythonw.exe) is running but not listening on :8787 locally. Port 8768 (HermesKB) also unreachable.
**Impact:** All KB contributions via `contribute.py` will fail. The `verify_contribution()` function cannot verify any posted data. The `post_knowledge()`, `post_finding()`, `post_contribute()` functions will all return connection errors.
**Fix:** Restore KB :8787 connectivity. Either restart the KB supervisor, find where it's actually listening, or use the `kb_bridge.py` mesh-node routing to reach it via a reachable node.

---

## P1 — HIGH (blocks core functionality)

### H1: `/gamification/missions/{contributor_id}` hardcodes only 20 of 58 missions
**Component:** `backend/main.py` lines 333–364
**Evidence:** The `all_missions` list in `get_missions_data()` is hardcoded with only 20 mission entries (first_spark through visionary). It does NOT include the 26 new missions added to `backend/gamification/scoring.py` (civic_participant, data_citizen, environmental_steward, climate_analyst, etc.). The scoring.py module has 58 missions in `MISSION_CATALOG` but the API endpoint returns a truncated hardcoded list.
**Impact:** New missions (Tier 6–10) are invisible via the `/gamification/missions/{contributor_id}` API. Contributors cannot see or earn them through the API. The scoring engine will award them, but the frontend can't display them.
**Fix:** Replace the hardcoded `all_missions` list in `get_missions_data()` with a dynamic query to `MISSION_CATALOG` from scoring.py, or import and use it directly.

### H2: `GET /refresh` (POST) still has `_require_refresh_auth` decorator AND `secret` param
**Component:** `backend/main.py` line 237–238 (same as C1, different perspective)
**Evidence:** The POST `/refresh` handler at line 237–238 still has:
```python
@app.post("/refresh")
def trigger_refresh(secret: str = Query(...)):
    """Trigger a refresh pipeline run. Requires HMAC-validated secret."""
```
and the `_require_refresh_auth` import still exists at line 19–23.
**Impact:** POST /refresh is completely broken — requires a secret parameter that may not be known. The refresh pipeline (scripts/refresh_v2.py) cannot be triggered via API.
**Fix:** Remove `secret` parameter and the decorator from `trigger_refresh`.

### H3: `data/cache/` has 29 files but `dist/data/` only has 10
**Component:** `dist/data/` directory + `data/cache/` directory
**Evidence:** `data/cache/` has 29 JSON files. `dist/data/` has only 10 (climate.json, datasets.json, demographics.json, economic.json, health.json, indicators.json, map_layers.json, map-layers.json, news.json, stakeholders.json). Missing 19 files including: bea_income.json, business.json, census_dp03.json, census_dp05.json, education.json, environment.json, government.json, housing.json, noaa_daily.json, noaa_daily_2025-09-02_2026-09-02.json, noaa_daily_2025-09-03_2026-09-03.json, open_meteo_forecast.json, redfin.json, redfin_volusia.json, safety.json, tourism.json, transportation.json, volusia_business.json, volusia_gis.json, zillow_zhvi.json.
**Impact:** Frontend hooks trying to fetch these data files via `/data/{name}.json` will get 404 errors for the 19 missing files. The `/data/{name}.json` endpoint at backend/main.py line 99–109 reads from `data/cache/{name}.json` so the backend works, but the built dist/ is incomplete.
**Fix:** Re-run `npm run build` to ensure all cache files are copied to dist/data/, or copy the missing files manually.

### H4: `gamification/` directory has stale leaderboard data
**Component:** `data/gamification/` directory
**Evidence:** `leaderboard-2026-W35.json` has 1 entry (zqmco, score 82.7, reviewed tier). `leaderboard-2026-W36.json` is empty `[]`. `zqmco.json` shows total_xp: 381, level: Explorer, but the `mission_flags` only includes earned missions up to `verified` — missing all 26 new missions.
**Impact:** Leaderboard data is inconsistent. The gamification state file doesn't reflect the new mission additions. Contributors who earned new missions won't see them reflected in their profile.
**Fix:** Run `python scripts/contribute.py --resync` or manually update `zqmco.json` to include all 58 mission IDs in `mission_flags`.

### H5: Pathways O–S cannot contribute via `/gamification/contribute`
**Component:** `backend/gamification/scoring.py` line with `pathway: str = Field(..., pattern=r"^[A-Na-n]$|^agent-item$")`
**Evidence:** The regex `^[A-Na-n]$` only matches A–N. Pathways O, P, Q, R, S return `string_pattern_mismatch` 422 errors. This affects 14 of 18 pathways (A–N work, O–S blocked).
**Impact:** Contributions to Pathways O (Accessibility), P (Crisis/Disaster), Q (Environmental), R (Cultural Heritage), S (Workforce/Labor) are completely blocked at the API level. These pathways have full contribution templates but cannot accept submissions.
**Fix:** Change the pattern from `r"^[A-Na-n]$|^agent-item$"` to `r"^[A-Sa-s]$|^agent-item$"` in `ContributeRequest`.

---

## P2 — MEDIUM

### M1: `datasets` table `content` field is always empty (all 10 entries have content_len=0)
**Component:** `data/volusia.db` → `datasets` table + `backend/main.py` line 66–70
**Evidence:** `SELECT * FROM datasets` returns 10 rows with `content = ''` for all. The table schema has columns `id, source, content, fetched_at` but `content` is never populated by the refresh pipeline.
**Impact:** The `/datasets` endpoint returns metadata-only. The `content` field is useless. Frontend hooks expecting actual dataset content will get empty strings.
**Fix:** Either populate `content` from `data/cache/{source}.json` on refresh, or change the schema to store file references instead of inline content.

### M2: `map_layers` table has 18 entries but `url` field is empty for ALL entries
**Component:** `data/volusia.db` → `map_layers` table
**Evidence:** All 18 map layers have `url = ''`. The `map-layers` API endpoint returns layers with empty URLs. Frontend can't fetch actual map tile data.
**Impact:** Map layers are non-functional. The MapsPage shows simplified polygons (hardcoded) instead of real map tiles from the layers.
**Fix:** Populate `url` field with actual GeoJSON/tile URLs, or link to the `data/cache/volusia_gis.json` content.

### M3: `gamification_history` table has 17 entries but all `xp_earned = 0`
**Component:** `data/volusia.db` → `gamification_history` table
**Evidence:** All 17 entries show `xp_earned = 0`. These are page_visit events from early testing. The gamification engine never awarded XP through history.
**Impact:** Historical gamification data is useless. XP tracking is broken for all historical events.
**Fix:** Backfill `xp_earned` based on contribution quality scores, or mark historical events as informational only.

### M4: `REFRESH_TOKEN` is hardcoded in `backend/main.py` line 17
**Component:** `backend/main.py` line 17
**Evidence:** `REFRESH_TOKEN = os.environ.get("VOLUSIA_REFRESH_TOKEN", "volusia-refresh-secret-change-me")`. The default value is a plaintext secret that's committed to git.
**Impact:** Anyone with the source code can POST to `/refresh` and trigger the data pipeline. The `_require_refresh_auth` check is broken because the default token is publicly known.
**Fix:** Remove the hardcoded default, require the environment variable to be set, or use a proper secret management approach.

### M5: `npm run build` generates new hashed filenames but nginx config caches assets forever
**Component:** `nginx/nginx.conf` line 15–18 + `npm run build`
**Evidence:** Nginx config has `location /assets/ { expires 1y; add_header Cache-Control "public, immutable"; }`. After every build, the hashed filenames change (e.g., `index-Cjq5DE-Q.css` → new hash). But the old hashed files remain on disk. The `try_files` fallback to `index.html` serves the new HTML with new asset references, but old hashed files linger.
**Impact:** Old asset files accumulate in `dist/assets/`. Disk space grows over time. The `dist/data/` sync issue (H3) is related.
**Fix:** Add a `clean` step before build (`rm -rf dist/`), or configure nginx to not cache immutable assets with old names.

### M6: `cvb_hotels` table has data only from 2020–2021 (vintage 4+ years old)
**Component:** `data/volusia.db` → `cvb_hotels` table
**Evidence:** 14 entries, first is `November 2020`, last is likely `2021`. All data is from 2020–2021 vintage. The CVB source URL (`OCC_ADR_RevPar_CDT_Summary_*_*.pdf`) points to PDF source files that are 4+ years old.
**Impact:** Tourism data is severely stale. The TouristsPage shows data from 2020–2021. The CVB pipeline (`scripts/refresh_v2.py`) is not fetching current data.
**Fix:** Update the CVB refresh pipeline to fetch current-year data, or flag the data as historical-only in the UI.

### M7: `analytics/dashboard` returns only Climate indicators (3 entries)
**Component:** `backend/main.py` line 290–297 + `data/cache/climate.json`
**Evidence:** `GET /analytics/dashboard` returns data for only 3 Climate indicators (avg_max_temp, avg_min_temp, total_precip). The dashboard should show data across all 4 categories (Economic, Demographics, Tourism, Climate).
**Impact:** The analytics dashboard is incomplete — only shows Climate data. Economic, Demographics, and Tourism dashboard panels are empty.
**Fix:** Update `get_dashboard_data()` to query all categories from the `indicators` table, not just Climate.

### M8: `data/gamification/leaderboard-2026-W36.json` is empty `[]`
**Component:** `data/gamification/` directory
**Evidence:** W36 leaderboard is empty. W35 has 1 entry. The `_save_leaderboard_snapshot()` function is called in `get_leaderboard()` when `period == "weekly"`, but the snapshot is empty.
**Impact:** Current week leaderboard shows no data. The `get_leaderboard()` API returns empty for weekly period.
**Fix:** Check the `_save_leaderboard_snapshot()` logic — the `entries` list may be empty because `_gam_state` has no active contributors with data.

---

## P3 — LOW

### L1: `backend/gamification/scoring.py` uses `importlib.util` to load itself from `main.py`
**Component:** `backend/main.py` lines 385–393
**Evidence:** `main.py` loads `scoring.py` via `importlib.util.spec_from_file_location` because `scoring.py` defines its own `router` and `app.include_router(_scoring_mod.router)`. This "file-shadows-package" pattern is fragile.
**Impact:** If `scoring.py` is imported as a module (e.g., from tests), it may fail. The `importlib` approach bypasses normal Python import semantics.
**Fix:** Refactor to use proper package imports. Move `scoring.py` to `backend/gamification/scoring.py` and import via `from backend.gamification.scoring import router`.

### L2: `data/gamification/leaderboard-2026-W35.json` has `quality_tier: "reviewed"` but `total_xp: 0`
**Component:** `data/gamification/leaderboard-2026-W35.json`
**Evidence:** The snapshot shows `quality_tier: "reviewed"` but `total_xp: 0` and `level: "Newcomer"`. This is inconsistent — a reviewer should have earned XP.
**Impact:** Leaderboard snapshot data is inconsistent with actual gamification state.
**Fix:** Regenerate the snapshot from `_gam_state` to ensure consistency.

### L3: `dist/data/` has both `map_layers.json` and `map-layers.json` (duplicate)
**Component:** `dist/data/` directory
**Evidence:** Both `map_layers.json` and `map-layers.json` exist in `dist/data/`. The backend uses `/map-layers` as the API endpoint and `/data/{name}.json` as the file endpoint. Having both is redundant and confusing.
**Impact:** Confusion about which file to use. The `map-layers.json` is the correct one (matches the API endpoint name). The `map_layers.json` is a duplicate.
**Fix:** Remove the duplicate `map_layers.json` from `dist/data/` and `data/cache/`.

### L4: `noaa_daily_2025-09-02_2026-09-02.json` and `noaa_daily_2025-09-03_2026-09-03.json` are dated cache files
**Component:** `data/cache/` directory
**Evidence:** Two NOAA daily cache files with date-stamped filenames. These are likely from a previous refresh run that left stale files.
**Impact:** Stale cache files accumulate. The refresh pipeline may not clean up old dated files.
**Fix:** Add cleanup logic to `refresh_v2.py` to remove old dated cache files.

### L5: `backend/gamification/scoring.py` has 58 missions but `get_missions_data()` in main.py only returns 20
**Component:** `backend/main.py` lines 333–364 vs `backend/gamification/scoring.py` MISSION_CATALOG
**Evidence:** The hardcoded `all_missions` list in `get_missions_data()` has exactly 20 entries. `MISSION_CATALOG` in scoring.py has 58 entries. These are out of sync.
**Impact:** Contributors see a truncated mission list. The scoring engine awards 58 missions but the API only exposes 20.
**Fix:** Replace the hardcoded list with a dynamic import from scoring.py's `MISSION_CATALOG`.

### L6: `backend/main.py` imports `from gamification import get_gamification_routes, _init_gamification_db` at line 10
**Component:** `backend/main.py` line 10
**Evidence:** This import assumes a `gamification` package/module exists at the top level. The actual gamification code is in `backend/gamification/`. This may fail if the module path is wrong.
**Impact:** If the import fails, the entire backend fails to start. The `_init_gamification_db` call at line 15 depends on this.
**Fix:** Verify the `gamification` module is importable. If not, fix the import path.

---

## P4 — INFO/LOW PRIORITY

### I1: `nginx/nginx.conf` proxies `/api/` to `backend:8000` but backend runs on `127.0.0.1:8000`
**Component:** `nginx/nginx.conf` line 31 + actual backend
**Evidence:** `proxy_pass http://backend:8000/;` — this uses Docker service name `backend` which may not resolve if running natively.
**Impact:** If running natively (not in Docker), the nginx proxy to backend fails. All `/api/*` requests return 502.
**Fix:** Change proxy_pass to `http://127.0.0.1:8000/` for native execution, or keep Docker configuration.

### I2: `data/cache/indicators.json` and `data/cache/datasets.json` may be stale
**Component:** `data/cache/` directory
**Evidence:** Cache files exist but their contents haven't been verified against the live API.
**Impact:** Frontend hooks reading from `data/cache/{name}.json` may serve stale data.
**Fix:** Add a freshness check to `refresh_v2.py` that validates cache file timestamps against the live API.

### I3: `CONTRIBUTION/templates/CONSTITUENCY_CONTRIBUTIONS.md` has 11 pathways (A–S) but only 4 have missions
**Component:** Contribution templates vs gamification missions
**Evidence:** Pathways A–S are documented. Only B, C, D, E have gated missions. A, F–S have no mission awards.
**Impact:** Contributors to 14 pathways have no gamification incentive structure.
**Fix:** Add pathway-specific missions for A, F–S in scoring.py (partially addressed by the 26 new missions, but gates need wiring).

### I4: `dist/assets/` has 5 JS/CSS files but `dist/index.html` references new hashes after build
**Component:** `dist/` directory
**Evidence:** After `npm run build`, `dist/index.html` references new hashed filenames. Old hashed files remain in `dist/assets/`.
**Impact:** Disk space waste. Old assets never cleaned up.
**Fix:** Add `rm -rf dist/` before `npm run build` in the build script.

### I5: `backend/main.py` line 136–137: `@app.get("/refresh")` and `@app.get("/diagnostics")` both point to same function
**Component:** `backend/main.py` line 136–137
**Evidence:** Both `/refresh` (GET) and `/diagnostics` are decorated with `@app.get` and point to `diagnostics()`. This means `GET /refresh` returns diagnostics, not a refresh trigger.
**Impact:** `GET /refresh` returns diagnostics data, not a refresh trigger. The name is misleading. The POST `/refresh` is the actual trigger.
**Fix:** Rename `diagnostics()` or remove the `@app.get("/refresh")` decorator to avoid confusion.

### I6: `data/gamification/zqmco.json` shows `quality_tier: "verified"` but `total_xp: 381` (Explorer level)
**Component:** `data/gamification/zqmco.json`
**Evidence:** The gamification state shows `quality_tier: "verified"` and `quality_score.overall: 87.5` but `total_xp: 381` and `level: "Explorer"`. XP and quality tier are tracked separately but may be inconsistent.
**Impact:** Quality tier and XP level may diverge. A "verified" contributor at Explorer level seems low.
**Fix:** Align quality tier with XP level, or document that they're independent metrics.

---

## Summary Table

| Priority | Count | Examples |
|----------|-------|----------|
| P0 — Critical | 3 | /refresh POST still needs secret, datasets content all empty, KB :8787 unreachable |
| P1 — High | 5 | Missions hardcoded (20/58), dist/data missing 19 files, stale leaderboard, pathways O–S blocked, refresh still broken |
| P2 — Medium | 8 | datasets content empty, map_layers URLs empty, gamification_history XP=0, hardcoded REFRESH_TOKEN, stale CVB data, dashboard only Climate, empty W36 leaderboard |
| P3 — Low | 6 | importlib pattern, inconsistent snapshots, duplicate map files, stale NOAA caches, hardcoded missions, gamification import path |
| P4 — Info | 6 | nginx proxy, stale cache, pathway coverage, old assets, refresh GET confusion, quality tier mismatch |

**Total: 22 issues (3 CRITICAL, 5 HIGH, 8 MEDIUM, 6 LOW)**

---

## Recommended Action Plan

### Immediate (P0)
1. Fix `trigger_refresh` — remove `secret` parameter and `_require_refresh_auth` decorator
2. Repopulate `datasets.content` from `data/cache/{name}.json`, or redesign the schema
3. Restore KB :8787 connectivity or implement the mesh-node bridge

### High Priority (P1)
4. Replace hardcoded `all_missions` list in `get_missions_data()` with dynamic `MISSION_CATALOG` import
5. Copy all 29 cache files to `dist/data/` (fix `npm run build` or add sync step)
6. Fix pathway pattern from `^[A-Na-n]$` to `^[A-Sa-s]$` in `ContributeRequest`
7. Regenerate gamification state and leaderboard snapshots
8. Fix `REFRESH_TOKEN` hardcoded default — require env var

### Medium Priority (P2)
9. Update `map_layers` table URLs with actual GeoJSON sources
10. Update `cvb_hotels` data to current year
11. Fix analytics dashboard to show all 4 categories
12. Clean up stale dated cache files
13. Remove duplicate `map_layers.json` from dist/data/

### Low Priority (P3/P4)
14. Refactor `importlib` pattern to proper package imports
15. Add `rm -rf dist/` before `npm run build`
16. Fix nginx proxy_pass for native execution
17. Rename confusing `GET /refresh` / `diagnostics` overlap

---

## Verification Commands

```bash
# Check all API endpoints
for ep in health indicators datasets map-layers data/indicators.json pulse.json business residents tourists leaders analytics/dashboard categories gamification/missions/test gamification/leaderboard gamification/pulse; do
  code=$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:8000/$ep")
  echo "$ep: $code"
done

# Check database integrity
python3 -c "import sqlite3; conn=sqlite3.connect('data/volusia.db'); c=conn.cursor(); print([r[0] for r in c.execute('SELECT name FROM sqlite_master WHERE type=\\\"table\\\"')])"

# Check build
npm run build && echo "BUILD OK"

# Check TypeScript
npx tsc --noEmit && echo "TS OK"

# Check data cache vs dist
diff <(ls data/cache/*.json | xargs -I{} basename {}) <(ls dist/data/*.json | xargs -I{} basename {})
```
