"""Project Volusia — FastAPI Backend v3
Serves real economic indicators from SQLite database + CSV downloads.
"""
import csv, io, json, os, sqlite3, subprocess, requests
import hmac, hashlib
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, JSONResponse
from gamification import get_gamification_routes, _init_gamification_db

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "volusia.db"
app = FastAPI(title="Project Volusia API", version="3.0.0")
# Initialize gamification tables
conn = sqlite3.connect(str(DB_PATH)); _init_gamification_db(conn); conn.close()

REFRESH_TOKEN = os.environ.get("VOLUSIA_REFRESH_TOKEN")
if not REFRESH_TOKEN:
    raise RuntimeError("VOLUSIA_REFRESH_TOKEN environment variable is required")

def _require_refresh_auth(secret: str = Query(...)):
    """HMAC-validated secret check. Raises 401 if invalid."""
    if not secret or not hmac.compare_digest(str(secret), REFRESH_TOKEN):
        raise HTTPException(status_code=401, detail="Authentication required")
    return True

app.add_middleware(
    CORSMiddleware, allow_origins=["https://zqmlabs.com", "https://www.zqmlabs.com", "http://localhost:8080", "http://127.0.0.1:8080"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"])

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
@_require_refresh_auth()
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

@app.get("/data/news.json")
def get_news_data():
    """Alias for /news.json — serves from /data prefix."""
    return get_news()

@app.post("/refresh")
@_require_refresh_auth()
def trigger_refresh():
    """Trigger a refresh pipeline run. Requires HMAC-validated secret."""
    try:
        proc = subprocess.run(["python", str(Path(__file__).parent.parent / "scripts" / "refresh_v2.py")], capture_output=True, text=True, timeout=300)
        return {"status": "triggered", "returncode": proc.returncode}
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
        b = _scoring_mod._badge_for_state(state)
        if b: badges.append(b)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
