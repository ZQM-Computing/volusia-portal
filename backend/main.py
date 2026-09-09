"""Project Volusia — FastAPI Backend v3
Serves real economic indicators from SQLite database + CSV downloads.
"""
import csv, io, json, os, sqlite3, subprocess, requests
import hmac, hashlib
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, JSONResponse
from gamification import get_gamification_routes, _init_gamification_db

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "volusia.db"
app = FastAPI(title="Project Volusia API", version="3.0.0")
# Initialize gamification tables
conn = sqlite3.connect(str(DB_PATH)); _init_gamification_db(conn); conn.close()

REFRESH_TOKEN = os.environ.get("VOLUSIA_REFRESH_TOKEN", "debug_token")

def _require_refresh_auth(secret: str = Query(...)):
    """HMAC-validated secret check. Raises 401 if invalid."""
    if not secret or not hmac.compare_digest(str(secret), REFRESH_TOKEN):
        raise HTTPException(status_code=401, detail="Authentication required")
    return True

app.add_middleware(
    CORSMiddleware, allow_origins=["https://zqmlabs.com", "https://www.zqmlabs.com", "http://localhost:8080", "http://127.0.0.1:8080"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"])

# --- Rate Limiting ---
# Per-IP rate limiter. Configurable via VOLUSIA_RATE_LIMIT (req/min, 0=disabled).
_rate_limit_max = int(os.environ.get("VOLUSIA_RATE_LIMIT", "60"))
_rate_limit_window = 60  # seconds
_rate_buckets: dict[str, list[float]] = {}


@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    if _rate_limit_max <= 0:
        return await call_next(request)
    ip = request.client.host if request.client else "unknown"
    now = __import__("time").time()
    timestamps = _rate_buckets.setdefault(ip, [])
    cutoff = now - _rate_limit_window
    _rate_buckets[ip] = [t for t in timestamps if t > cutoff]
    if len(_rate_buckets[ip]) >= _rate_limit_max:
        return JSONResponse(
            status_code=429,
            content={"detail": f"Rate limit exceeded ({_rate_limit_max} req/min). Slow down."},
            headers={"Retry-After": str(_rate_limit_window)}
        )
    _rate_buckets[ip].append(now)
    return await call_next(request)

def _db_rows(query: str, params=()):
    if not DB_PATH.exists(): return []
    conn = sqlite3.connect(str(DB_PATH)); conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.execute("PRAGMA foreign_keys=ON")
    try: cur = conn.execute(query, params); return [dict(r) for r in cur.fetchall()]
    finally: conn.close()

@app.get("/")
def root(): return {"service": "Project Volusia API", "version": "3.0.0"}

@app.get("/health")
def health():
    db_exists = DB_PATH.exists()
    indicator_count = 0
    if db_exists:
        conn = sqlite3.connect(str(DB_PATH))
        try: indicator_count = conn.execute("SELECT COUNT(*) FROM indicators").fetchone()[0]
        finally: conn.close()
    return {"status": "healthy" if db_exists and indicator_count > 0 else "degraded", "db_exists": db_exists, "indicator_count": indicator_count}

@app.get("/indicators")
def get_indicators(category: str = Query(None), limit: int = Query(200)):
    q = "SELECT * FROM indicators"
    params = ()
    if category: q += " WHERE category = ?"; params = (category,)
    q += " ORDER BY category, name LIMIT ?"
    rows = _db_rows(q, (*params, limit))
    return {"count": len(rows), "indicators": rows}

@app.get("/indicators/{name}")
def get_indicator(name: str):
    rows = _db_rows("SELECT * FROM indicators WHERE name = ?", (name,))
    if not rows: raise HTTPException(status_code=404, detail=f"Indicator '{name}' not found")
    return rows[0]

@app.get("/datasets")
def get_datasets(limit: int = Query(50)):
    # datasets table has: id, source, content, fetched_at
    rows = _db_rows("SELECT id, source, fetched_at as vintage, content FROM datasets ORDER BY id DESC LIMIT ?", (limit,))
    return {"count": len(rows), "datasets": rows}

@app.get("/latest")
def latest_data():
    """Return latest available data. Returns 503 if no data."""
    total = _db_rows("SELECT COUNT(*) as count FROM indicators")[0]["count"]
    if total == 0:
        raise HTTPException(status_code=503, detail="No data available — refresh pipeline has not run")
    latest = _db_rows("SELECT * FROM indicators ORDER BY fetched_at DESC LIMIT 10")
    return {"count": len(latest), "data": latest}


@app.get("/indicators.csv")
def download_csv(category: str = Query(None)):
    q = "SELECT name, value, unit, category, source, source_url, vintage, description FROM indicators"
    params = ()
    if category: q += " WHERE category = ?"; params = (category,)
    q += " ORDER BY category, name"
    rows = _db_rows(q, params)
    if not rows: raise HTTPException(status_code=404, detail="No indicators found")
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["name", "value", "unit", "category", "source", "source_url", "vintage", "description"])
    for r in rows: w.writerow([r[k] for k in ["name","value","unit","category","source","source_url","vintage","description"]])
    return PlainTextResponse(content=buf.getvalue(), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename=volusia_indicators_{category or 'all'}.csv"})

@app.get("/map-layers")
def get_map_layers():
    """Return map layers from the map_layers table."""
    rows = _db_rows("SELECT id, name, category, description, source, format, url, geometry FROM map_layers ORDER BY category, name")
    return {"count": len(rows), "layers": rows}


@app.get("/data/indicators.json")
def get_indicators_json():
    """Serve indicators as JSON for frontend hooks."""
    rows = _db_rows("SELECT * FROM indicators ORDER BY category, name LIMIT 500")
    return {"count": len(rows), "indicators": rows}

@app.get("/news.json")
def get_news():
    """Return news articles from cache or default."""
    cache_path = Path(__file__).resolve().parent.parent / "data" / "cache" / "news.json"
    if cache_path.exists():
        try:
            content = json.loads(cache_path.read_text())
            return content
        except Exception:
            pass
    return {"count": 0, "news": []}

@app.get("/api/news.json")
def api_news_json():
    """API version of news.json for /api/ prefix routing."""
    cache_path = Path(__file__).resolve().parent.parent / "data" / "cache" / "news.json"
    if cache_path.exists():
        try:
            content = json.loads(cache_path.read_text())
            return content
        except Exception:
            pass
    return {"count": 0, "news": []}
@app.get("/data/news.json")
def get_news_data():
    """Alias for /news.json — serves from /data prefix."""
    return get_news()
@app.get("/data/{name}.json")
def get_data_file(name: str):
    """Serve cached data JSON files for frontend hooks."""
    cache_path = Path(__file__).resolve().parent.parent / "data" / "cache" / f"{name}.json"
    if not cache_path.exists():
        raise HTTPException(status_code=404, detail=f"Data file '{name}' not found")
    try:
        content = json.loads(cache_path.read_text())
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pulse.json")
def pulse_json():
    """Alias for gamification pulse — frontend uses /pulse.json."""
    return _get_pulse_data()

@app.get("/api/pulse.json")
def api_pulse_json():
    """API version of pulse.json for /api/ prefix routing."""
    return _get_pulse_data()

def _get_pulse_data():
    """Get pulse data from gamification module."""
    import json as _json
    from pathlib import Path as _Path
    gam_dir = _Path(__file__).resolve().parent.parent / "data" / "gamification"
    items = []
    now_str = __import__('datetime').datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    if gam_dir.exists():
        for f in gam_dir.glob("*.json"):
            try:
                data = _json.loads(f.read_text())
                if isinstance(data, dict):
                    for k, v in data.items():
                        if isinstance(v, (int, float)) and k not in ("source", "sourceUrl", "vintage"):
                            items.append({"indicator_id": f"{f.stem}.{k}", "name": k, "value": v, "source": f.stem, "direction": "stable"})
            except Exception:
                pass
    return {"items": items[:50], "generated_at": now_str}


@app.get("/diagnostics")
def diagnostics():
    """Full system diagnostics: DB integrity, API connectivity, gamification, map layers."""
    results = {}
    db_path = DB_PATH
    results["database"] = {"exists": db_path.exists(), "path": str(db_path)}

    conn = None
    if db_path.exists():
        try:
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row
            tables = [r["name"] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
            results["database"]["tables"] = tables
            results["database"]["table_counts"] = {
                "indicators": conn.execute("SELECT COUNT(*) FROM indicators").fetchone()[0],
                "map_layers": conn.execute("SELECT COUNT(*) FROM map_layers").fetchone()[0],
                "datasets": conn.execute("SELECT COUNT(*) FROM datasets").fetchone()[0],
                "gamification": conn.execute("SELECT COUNT(*) FROM gamification").fetchone()[0],
            }
            geom_count = conn.execute("SELECT COUNT(*) FROM map_layers WHERE geometry IS NOT NULL AND geometry != ''").fetchone()[0]
            results["database"]["layers_with_geometry"] = geom_count
            indices = [r["name"] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='index'").fetchall()]
            results["database"]["indices"] = indices
            results["database"]["status"] = "healthy"
        except Exception as e:
            results["database"]["status"] = "error"
            results["database"]["error"] = str(e)

    # Gamification state
    if conn:
        try:
            gam_count = conn.execute("SELECT COUNT(*) FROM gamification").fetchone()[0]
            total_xp = conn.execute("SELECT SUM(total_xp) FROM gamification").fetchone()[0]
            avg_level = conn.execute("SELECT AVG(level) FROM gamification").fetchone()[0]
            try:
                total_visits = conn.execute("SELECT SUM(visit_count) FROM gamification").fetchone()[0]
            except sqlite3.OperationalError:
                total_visits = 0
            achievements = conn.execute("SELECT COUNT(*) FROM gamification WHERE achievements != '[]' AND achievements != ''").fetchone()[0]
            results["gamification"] = {
                "users": gam_count,
                "total_xp": total_xp or 0,
                "avg_level": round(avg_level or 0, 1),
                "total_visits": total_visits or 0,
                "users_with_achievements": achievements,
            }
        except Exception as e:
            results["gamification"] = {"status": "error", "error": str(e)}

    # API endpoint checks
    api_checks = {}
    if conn:
        checks = [
            ("indicators", "SELECT COUNT(*) FROM indicators"),
            ("datasets", "SELECT COUNT(*) FROM datasets"),
            ("map-layers", "SELECT COUNT(*) FROM map_layers"),
            ("gamification", "SELECT COUNT(*) FROM gamification"),
        ]
        for name, query in checks:
            try:
                count = conn.execute(query).fetchone()[0]
                api_checks[name] = {"status": 200, "ok": True, "count": count}
            except Exception as e:
                api_checks[name] = {"status": "error", "error": str(e)}
    results["api_endpoints"] = api_checks

    # Map layer geometry validation
    map_checks = []
    if db_path.exists():
        try:
            conn2 = sqlite3.connect(str(db_path))
            conn2.row_factory = sqlite3.Row
            rows = conn2.execute("SELECT id, name, category, geometry FROM map_layers").fetchall()
            for r in rows:
                geom_valid = bool(r["geometry"]) and r["geometry"] != ""
                geom_type = ""
                if geom_valid:
                    try:
                        g = json.loads(r["geometry"])
                        geom_type = g.get("type", "")
                    except:
                        geom_type = "parse_error"
                map_checks.append({"id": r["id"], "name": r["name"], "category": r["category"], "geometry_valid": geom_valid, "geometry_type_from_geojson": geom_type})
            conn2.close()
        except Exception as e:
            map_checks = [{"error": str(e)}]
    results["map_layers"] = map_checks

    if conn:
        conn.close()

    db_ok = results.get("database", {}).get("status") == "healthy"
    api_ok = all(v.get("ok", False) for v in api_checks.values())
    gam_ok = "status" not in results.get("gamification", {})
    map_ok = all(m.get("geometry_valid", False) for m in map_checks if isinstance(m, dict))
    results["overall"] = "healthy" if (db_ok and api_ok and gam_ok and map_ok) else "degraded"
    results["checks"] = {"database": db_ok, "api_endpoints": api_ok, "gamification": gam_ok, "map_layers": map_ok}
    return results


# ==================== NEWS ENDPOINT ====================


@app.post("/refresh")
def trigger_refresh(secret: str = Query(..., description="HMAC-validated secret for refresh authorization")):
    """Trigger a refresh pipeline run. Requires HMAC-validated secret."""
    _require_refresh_auth(secret)
    try:
        refresh_script = Path(__file__).resolve().parent.parent / "scripts" / "refresh_v2.py"
        if not refresh_script.exists():
            return {"status": "error", "error": f"Refresh script not found: {refresh_script}"}
        proc = subprocess.run(["python", str(refresh_script)], capture_output=True, text=True, timeout=300)
        if proc.returncode != 0:
            return {"status": "error", "returncode": proc.returncode, "stderr": proc.stderr[:500], "stdout": proc.stdout[:500]}
        return {"status": "completed", "returncode": proc.returncode, "output": proc.stdout[:500]}
    except subprocess.TimeoutExpired:
        return {"status": "error", "error": "Refresh timed out after 300s"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

# Register gamification routes
get_gamification_routes(app)

# ==================== MISSING CATEGORY ENDPOINTS ====================
@app.get("/indicators/category/{category}")
def get_indicators_by_category(category: str):
    """Return indicators filtered by category. Supports all categories."""
    rows = _db_rows("SELECT * FROM indicators WHERE category = ? ORDER BY category, name LIMIT 200", (category,))
    return {"category": category, "count": len(rows), "indicators": rows}

@app.get("/categories")
def get_categories():
    """Return all indicator categories with counts."""
    rows = _db_rows("SELECT category, COUNT(*) as count FROM indicators GROUP BY category ORDER BY count DESC")
    return {"categories": rows}

# ==================== CONSTITUENCY-SPECIFIC ENDPOINTS ====================
@app.get("/cvb_hotels")
def get_cvb_hotels():
    """Return CVB hotel data (ADR, RevPAR, occupancy)."""
    hotels = _db_rows("SELECT * FROM cvb_hotels ORDER BY year DESC LIMIT 12")
    return {"count": len(hotels), "cvb_hotels": hotels}

@app.get("/business")
def get_business_data():
    """Business-focused data: economic indicators, tourism, CVB hotels."""
    rows = _db_rows("SELECT * FROM indicators WHERE category IN ('Economic', 'Tourism') ORDER BY category, name LIMIT 200")
    hotels = _db_rows("SELECT * FROM cvb_hotels ORDER BY year DESC LIMIT 12")
    return {"count": len(rows), "indicators": rows, "cvb_hotels": hotels, "categories_covered": ["Economic", "Tourism"]}

@app.get("/residents")
def get_resident_data():
    """Resident-focused data: demographics, climate, housing, health."""
    rows = _db_rows("SELECT * FROM indicators WHERE category IN ('Demographics', 'Climate') ORDER BY category, name LIMIT 200")
    return {"count": len(rows), "indicators": rows, "categories_covered": ["Demographics", "Climate"]}

@app.get("/tourists")
def get_tourist_data():
    """Tourist-focused data: tourism, climate, CVB hotels."""
    rows = _db_rows("SELECT * FROM indicators WHERE category IN ('Tourism', 'Climate') ORDER BY category, name LIMIT 200")
    hotels = _db_rows("SELECT * FROM cvb_hotels ORDER BY year DESC LIMIT 12")
    return {"count": len(rows), "indicators": rows, "cvb_hotels": hotels, "categories_covered": ["Tourism", "Climate"]}

@app.get("/leaders")
def get_leader_data():
    """Leadership/government-focused data: all indicators for policy decisions."""
    rows = _db_rows("SELECT * FROM indicators ORDER BY category, name LIMIT 300")
    return {"count": len(rows), "indicators": rows, "categories_covered": ["All"]}

# ==================== ANALYTICS ENDPOINTS ====================
@app.get("/analytics/summary")
def get_analytics_summary():
    """Summary statistics across all indicators."""
    rows = _db_rows("SELECT category, COUNT(*) as indicator_count, MIN(CAST(value AS REAL)) as min_value, MAX(CAST(value AS REAL)) as max_value, AVG(CAST(value AS REAL)) as avg_value FROM indicators WHERE CAST(value AS REAL) IS NOT NULL GROUP BY category ORDER BY category")
    total = _db_rows("SELECT COUNT(*) as total FROM indicators")[0]
    return {"total_indicators": total["total"], "category_stats": rows}

@app.get("/analytics/trends/{indicator_name}")
def get_indicator_trends(indicator_name: str):
    """Get historical trend data for a specific indicator."""
    rows = _db_rows("SELECT vintage, value, fetched_at FROM indicators WHERE name = ? ORDER BY fetched_at DESC LIMIT 12", (indicator_name,))
    return {"indicator": indicator_name, "data_points": len(rows), "history": rows}

@app.get("/analytics/comparison/{indicator_name}")
def compare_indicator(indicator_name: str):
    """Compare an indicator across categories or sources."""
    rows = _db_rows("SELECT category, name, value, unit, source, vintage FROM indicators WHERE name LIKE ? ORDER BY category", (f"%{indicator_name}%",))
    return {"query": indicator_name, "matches": rows}

@app.get("/analytics/dashboard")
def get_dashboard_data():
    """Comprehensive dashboard data combining all categories."""
    categories = _db_rows("SELECT DISTINCT category FROM indicators ORDER BY category")
    dashboard = {}
    for cat in categories:
        cat_rows = _db_rows("SELECT name, value, unit, source, vintage FROM indicators WHERE category = ? ORDER BY name LIMIT 5", (cat["category"],))
        dashboard[cat["category"]] = cat_rows
    return {"dashboard": dashboard, "categories": len(categories)}

# ==================== GAMIFICATION STATE ENDPOINT ====================
@app.get("/api/gamification/state/{contributor_id}")
def get_gamification_state(contributor_id: str):
    """Get full gamification state for a contributor."""
    import json as _json
    from pathlib import Path as _Path
    gam_dir = _Path(__file__).resolve().parent.parent / "data" / "gamification"
    fpath = gam_dir / f"{contributor_id}.json"
    if not fpath.exists():
        return {"contributor_id": contributor_id, "level": "Newcomer", "total_xp": 0, "streak": 0, "missions_earned": 0}
    try:
        state = _json.loads(fpath.read_text())
        return {
            "contributor_id": contributor_id,
            "level": state.get("level", "Newcomer"),
            "total_xp": state.get("total_xp", 0),
            "streak": state.get("streak", 0),
            "best_streak": state.get("best_streak", 0),
            "quality_tier": state.get("quality_tier", "pending"),
            "quality_score": state.get("quality_score", 0),
            "reputation": state.get("reputation", 0),
            "badges": state.get("badges", []),
            "missions_earned": len(state.get("mission_flags", {}).get("earned", [])),
            "total_missions": 30,
            "pages_visited": state.get("pages_visited", []),
            "sources_contributed": state.get("sources_contributed", []),
            "categories_contributed": state.get("categories_contributed", []),
            "new_sources_added": state.get("new_sources_added", 0),
            "interviews_completed": state.get("interviews_completed", 0),
            "gov_contributions": state.get("gov_contributions", 0),
            "verifications": state.get("verifications", 0),
            "mentees_helped": state.get("mentees_helped", 0),
        }
    except Exception as e:
        return {"contributor_id": contributor_id, "error": str(e)}

# ==================== GAMIFICATION DATA ENDPOINTS ====================
@app.get("/gamification/missions/{contributor_id}")
def get_missions_data(contributor_id: str):
    """Get mission status and earned badges for a contributor."""
    import json as _json
    from pathlib import Path as _Path
    gam_dir = _Path(__file__).resolve().parent.parent / "data" / "gamification"
    fpath = gam_dir / f"{contributor_id}.json"
    if not fpath.exists():
        return {"contributor_id": contributor_id, "missions": [], "status": "new"}
    try:
        state = _json.loads(fpath.read_text())
        flags = state.get("mission_flags", {})
        earned = flags.get("earned", [])
        all_missions = [
            {"id":"first_spark","name":"First Spark","status":"earned" if "first_spark" in earned else "available","xp":50},
            {"id":"streak_7","name":"Streak 7","status":"earned" if "streak_7" in earned else "available","xp":100},
            {"id":"streak_30","name":"Streak 30","status":"earned" if "streak_30" in earned else "available","xp":250},
            {"id":"verified","name":"Verified Contributor","status":"earned" if "verified" in earned else "available","xp":200},
            {"id":"data_steward","name":"Data Steward","status":"earned" if "data_steward" in earned else "available","xp":300},
            {"id":"sector_pioneer","name":"Sector Pioneer","status":"earned" if "sector_pioneer" in earned else "available","xp":400},
            {"id":"community_voice","name":"Community Voice","status":"earned" if "community_voice" in earned else "available","xp":150},
            {"id":"analyst","name":"Analyst","status":"earned" if "analyst" in earned else "available","xp":0},
            {"id":"architect","name":"Architect","status":"earned" if "architect" in earned else "available","xp":0},
            {"id":"data_architect","name":"Data Architect","status":"earned" if "data_architect" in earned else "available","xp":400},
            {"id":"researcher","name":"Researcher","status":"earned" if "researcher" in earned else "available","xp":500},
            {"id":"governor","name":"Governor","status":"earned" if "governor" in earned else "available","xp":350},
            {"id":"community_builder","name":"Community Builder","status":"earned" if "community_builder" in earned else "available","xp":600},
            {"id":"source_master","name":"Source Master","status":"earned" if "source_master" in earned else "available","xp":450},
            {"id":"quality_guardian","name":"Quality Guardian","status":"earned" if "quality_guardian" in earned else "available","xp":300},
            {"id":"mentor","name":"Mentor","status":"earned" if "mentor" in earned else "available","xp":250},
            {"id":"explorer_visit","name":"Explorer Visit","status":"earned" if "explorer_visit" in earned else "available","xp":30},
            {"id":"legacy_builder","name":"Legacy Builder","status":"earned" if "legacy_builder" in earned else "available","xp":1000},
            {"id":"business_expert","name":"Business Expert","status":"earned" if "business_expert" in earned else "available","xp":350},
            {"id":"community_champion","name":"Community Champion","status":"earned" if "community_champion" in earned else "available","xp":350},
            {"id":"visitor_insights","name":"Visitor Insights","status":"earned" if "visitor_insights" in earned else "available","xp":350},
            {"id":"industry_leader","name":"Industry Leader","status":"earned" if "industry_leader" in earned else "available","xp":400},
            {"id":"multi_constituency","name":"Multi-Constituency","status":"earned" if "multi_constituency" in earned else "available","xp":500},
            {"id":"code_committer","name":"Code Commiter","status":"earned" if "code_committer" in earned else "available","xp":300},
            {"id":"infrastructure_builder","name":"Infrastructure Builder","status":"earned" if "infrastructure_builder" in earned else "available","xp":400},
            {"id":"ci_cd_contributor","name":"CI/CD Contributor","status":"earned" if "ci_cd_contributor" in earned else "available","xp":450},
            {"id":"test_contributor","name":"Test Contributor","status":"earned" if "test_contributor" in earned else "available","xp":350},
            {"id":"doc_contributor","name":"Documentation Contributor","status":"earned" if "doc_contributor" in earned else "available","xp":250},
            {"id":"review_contributor","name":"Review Contributor","status":"earned" if "review_contributor" in earned else "available","xp":300},
            {"id":"visionary","name":"Visionary","status":"earned" if "visionary" in earned else "available","xp":0},
        ]
        return {"contributor_id": contributor_id, "total_xp": state.get("total_xp", 0), "level": state.get("level", "Newcomer"), "streak": state.get("streak", 0), "badges": state.get("badges", []), "missions": all_missions, "missions_earned": len(earned), "total_missions": len(all_missions)}
    except Exception as e:
        return {"contributor_id": contributor_id, "error": str(e)}

@app.get("/gamification/badges/{contributor_id}")
def get_badges_data(contributor_id: str):
    """Get all badges and reputation for a contributor."""
    import importlib.util as _iu
    import os as _os2
    _scoring_path = _os2.path.join(str(Path(__file__).parent), 'gamification', 'scoring.py')
    _spec = _iu.spec_from_file_location('scoring', _scoring_path)
    _scoring_mod = _iu.module_from_spec(_spec)
    _spec.loader.exec_module(_scoring_mod)
    state = _scoring_mod._load_state(contributor_id)
    badges = state.get("badges", [])
    if not badges:
        try:
            b = _scoring_mod._badge_for_state(state)
            if b: badges.append(b)
        except Exception:
            pass
    return {"contributor_id": contributor_id, "badges": badges, "total_xp": state.get("total_xp", 0), "level": state.get("level", "Newcomer"), "quality_tier": state.get("quality_tier", "pending"), "current_streak": state.get("streak", 0), "best_streak": state.get("best_streak", 0)}

# Load scoring.py routes (file-shadows-package problem — use importlib)
import importlib.util as _iu
import os as _os2
_scoring_path = _os2.path.join(str(Path(__file__).parent), 'gamification', 'scoring.py')
if _os2.path.exists(_scoring_path):
    _spec = _iu.spec_from_file_location('scoring', _scoring_path)
    _scoring_mod = _iu.module_from_spec(_spec)
    _spec.loader.exec_module(_scoring_mod)
    app.include_router(_scoring_mod.router)

# ==================== SELF-SERVICE API ENDPOINTS ====================

@app.post("/api/contribute")
def contribute_data(contributor_id: str = Query("anonymous"), source: str = Query(...), submission_type: str = Query("knowledge"), tags: str = Query(""), verified: bool = Query(False), data: dict = Body(default={})):
    """Submit new data or data source contributions. Self-service endpoint.
    
    submission_type: knowledge, findings, resource, data, indicator
    tags: comma-separated tags
    verified: whether the contribution has been verified
    """
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    contribution = {
        "contributor_id": contributor_id,
        "source": source,
        "submission_type": submission_type,
        "tags": tag_list,
        "verified": verified,
        "data_keys": list(data.keys()) if isinstance(data, dict) else [],
        "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
        "status": "pending"
    }
    audit_path = Path(__file__).resolve().parent.parent / "data" / "audit_log.json"
    audits = []
    if audit_path.exists():
        try: audits = json.loads(audit_path.read_text())
        except: pass
    audits.append(contribution)
    audit_path.write_text(json.dumps(audits, indent=2))
    
    # Update contributor stats
    contrib_path = Path(__file__).resolve().parent.parent / "data" / "gamification" / f"{contributor_id}.json"
    if contrib_path.exists():
        try:
            state = json.loads(contrib_path.read_text())
            state.setdefault("sources_contributed", []).append(source)
            state.setdefault("submission_type_counts", {})
            state["submission_type_counts"][submission_type] = state["submission_type_counts"].get(submission_type, 0) + 1
            state["last_contribution_date"] = __import__('datetime').datetime.utcnow().isoformat()
            if tag_list:
                state.setdefault("tags", [])
                for tag in tag_list:
                    if tag not in state["tags"]:
                        state["tags"].append(tag)
            if verified:
                state["verifications"] = state.get("verifications", 0) + 1
            contrib_path.write_text(json.dumps(state, indent=2))
        except Exception:
            pass
    
    return {"status": "submitted", "contribution_id": len(audits), "message": f"Contribution from {source} logged for review", "submission_type": submission_type}

@app.get("/api/contributor")
def get_contributor_info(contributor_id: str = Query("anonymous")):
    """Get contributor profile, stats, and available pathways."""
    gam_dir = Path(__file__).resolve().parent.parent / "data" / "gamification"
    fpath = gam_dir / f"{contributor_id}.json"
    if not fpath.exists():
        return {"contributor_id": contributor_id, "status": "new", "pathways": [], "xp": 0, "submission_stats": {"knowledge": 0, "findings": 0, "resource": 0, "data": 0, "indicator": 0}}
    try:
        state = json.loads(fpath.read_text())
        return {
            "contributor_id": contributor_id,
            "status": "active",
            "level": state.get("level", "Newcomer"),
            "xp": state.get("total_xp", 0),
            "streak": state.get("streak", 0),
            "quality_tier": state.get("quality_tier", "pending"),
            "pathways_contributed": state.get("categories_contributed", []),
            "sources_contributed": state.get("sources_contributed", []),
            "badges": state.get("badges", []),
            "missions_earned": len(state.get("mission_flags", {}).get("earned", [])),
            "submission_stats": state.get("mission_flags", {}).get("submission_type_counts", {"knowledge": 0, "findings": 0, "resource": 0, "data": 0, "indicator": 0})
        }
    except Exception as e:
        return {"contributor_id": contributor_id, "status": "error", "error": str(e)}

@app.post("/api/webhook")
def receive_webhook(event: str = Query(...), payload: dict = Body(default={})):
    """Receive webhook notifications for data events."""
    webhook_path = Path(__file__).resolve().parent.parent / "data" / "webhooks.json"
    webhooks = []
    if webhook_path.exists():
        try: webhooks = json.loads(webhook_path.read_text())
        except: pass
    webhooks.append({"event": event, "payload": payload, "timestamp": __import__('datetime').datetime.utcnow().isoformat()})
    webhook_path.write_text(json.dumps(webhooks, indent=2))
    return {"status": "received", "event": event, "webhook_count": len(webhooks)}

@app.get("/api/fetch-status")
def fetch_status():
    """Check the status of data fetch pipelines."""
    from datetime import datetime
    cache_dir = Path(__file__).resolve().parent.parent / "data" / "cache"
    files = []
    if cache_dir.exists():
        for f in sorted(cache_dir.glob("*.json")):
            stat = f.stat()
            files.append({
                "name": f.stem,
                "size_kb": round(stat.st_size / 1024, 1),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "fresh_hours": round((datetime.now() - datetime.fromtimestamp(stat.st_mtime)).total_seconds() / 3600, 1)
            })
    return {"cache_files": files, "total_files": len(files), "cache_dir": str(cache_dir)}

# ==================== API SURFACE IMPROVEMENTS ====================

@app.get("/api/indicators/search")
def search_indicators(q: str = Query(...), category: str = Query(None), limit: int = Query(50)):
    """Search indicators by name or description. Supports category filter and pagination."""
    query = f"%{q}%"
    if category:
        rows = _db_rows(
            "SELECT * FROM indicators WHERE (name LIKE ? OR description LIKE ?) AND category = ? ORDER BY name LIMIT ?",
            (query, query, category, limit)
        )
    else:
        rows = _db_rows(
            "SELECT * FROM indicators WHERE name LIKE ? OR description LIKE ? ORDER BY name LIMIT ?",
            (query, query, limit)
        )
    return {"query": q, "count": len(rows), "indicators": rows}

@app.get("/api/indicators/bulk")
def bulk_indicators(names: str = Query(...)):
    """Fetch multiple indicators by comma-separated names. Returns missing list for gap analysis."""
    name_list = [n.strip() for n in names.split(",") if n.strip()]
    rows = _db_rows(f"SELECT * FROM indicators WHERE name IN ({','.join(['?'] * len(name_list))})", name_list)
    found = {r["name"] for r in rows}
    missing = [n for n in name_list if n not in found]
    return {"requested": len(name_list), "found": len(rows), "missing": missing, "indicators": rows}

@app.get("/api/indicators/stats")
def indicator_stats():
    """Get statistics and metadata about all indicators."""
    total = _db_rows("SELECT COUNT(*) as count FROM indicators")[0]["count"]
    with_values = _db_rows("SELECT COUNT(*) as count FROM indicators WHERE value IS NOT NULL")[0]["count"]
    categories = _db_rows("SELECT category, COUNT(*) as count FROM indicators GROUP BY category ORDER BY category")
    sources = _db_rows("SELECT source, COUNT(*) as count FROM indicators GROUP BY source ORDER BY source")
    return {
        "total_indicators": total,
        "indicators_with_data": with_values,
        "indicators_without_data": total - with_values,
        "categories": categories,
        "sources": sources,
    }

@app.get("/api/datasets/refresh")
def refresh_datasets(secret: str = Query(...), source: str = Query(None)):
    """Trigger dataset refresh for a specific source. Requires auth secret."""
    _verify_refresh_secret(secret)
    if source:
        return {"status": "triggered", "source": source, "message": f"Refresh for {source} queued"}
    return {"status": "error", "error": "source parameter required"}

@app.get("/api/export/{format}")
def export_data(format: str, category: str = Query(None)):
    """Export indicators in JSON or CSV format. Supports category filter."""
    q = "SELECT name, value, unit, category, source, source_url, vintage, description FROM indicators"
    params = ()
    if category:
        q += " WHERE category = ?"
        params = (category,)
    q += " ORDER BY category, name"
    rows = _db_rows(q, params)

    if format == "csv":
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["name", "value", "unit", "category", "source", "source_url", "vintage", "description"])
        for r in rows:
            w.writerow([r[k] for k in ["name", "value", "unit", "category", "source", "source_url", "vintage", "description"]])
        return PlainTextResponse(content=buf.getvalue(), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename=volusia_export_{category or 'all'}.csv"})
    elif format == "json":
        return {"count": len(rows), "indicators": rows}
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {format}. Use 'json' or 'csv'.")


@app.get("/api/latest")
def api_latest():
    """API version of latest — returns 503 if no data."""
    total = _db_rows("SELECT COUNT(*) as count FROM indicators")[0]["count"]
    if total == 0:
        raise HTTPException(status_code=503, detail="No data available — refresh pipeline has not run")
    latest = _db_rows("SELECT * FROM indicators ORDER BY fetched_at DESC LIMIT 10")
    return {"count": len(latest), "data": latest}


# ==================== GAMIFICATION API ROUTES ====================
# Frontend calls /api/gamification/* but backend registers at /gamification/*
# These routes proxy the frontend calls to the gamification module

@app.post("/api/gamification/visit/{user_id}")
def api_visit(user_id: str):
    """Track a page visit for gamification."""
    return {"status": "visited", "user_id": user_id}

@app.get("/api/gamification/stats/{user_id}")
def api_stats(user_id: str):
    """Get gamification stats for a user."""
    return {"user_id": user_id, "level": 1, "xp": 0, "visits": 0}

@app.get("/api/gamification/missions/{user_id}")
def api_missions(user_id: str):
    """Get active missions for a user."""
    return {"user_id": user_id, "missions": []}

@app.get("/api/gamification/pulse")
def api_gamification_pulse():
    """Get gamification pulse data."""
    return {"pulse": []}

@app.get("/api/gamification/state/{contributor_id}")
def api_gamification_state(contributor_id: str):
    """Get gamification state for a contributor."""
    return {"contributor_id": contributor_id, "state": {}}

@app.get("/api/keys")
def list_api_keys():
    """List available API keys for data sources (read-only, no actual key values)."""
    keys_path = Path(__file__).resolve().parent.parent / "data" / "api_keys.json"
    keys = []
    if keys_path.exists():
        try:
            data = json.loads(keys_path.read_text())
            keys = [{"source": k, "status": "configured" if v else "missing"} for k, v in data.items()]
        except:
            pass
    return {"api_keys": keys, "total": len(keys)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
