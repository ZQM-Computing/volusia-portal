"""Project Volusia — FastAPI Backend v3
Serves real economic indicators from SQLite database + CSV downloads.
"""
import csv, io, os, sqlite3, requests
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, JSONResponse
from gamification import get_gamification_routes, _init_gamification_db

DB_PATH = Path(__file__).parent / "data" / "volusia.db"
app = FastAPI(title="Project Volusia API", version="3.0.0")
# Initialize gamification tables
conn = sqlite3.connect(str(DB_PATH)); _init_gamification_db(conn); conn.close()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"])

def _db_rows(query: str, params=()):
    if not DB_PATH.exists(): return []
    conn = sqlite3.connect(str(DB_PATH)); conn.row_factory = sqlite3.Row
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
    rows = _db_rows("SELECT id, name, source, source_url, vintage FROM indicators ORDER BY id DESC LIMIT ?", (limit,))
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

@app.get("/refresh")
@app.get("/diagnostics")
def diagnostics():
    """Full system diagnostics: DB integrity, API connectivity, gamification, map layers."""
    results = {}
    conn = None
    
    # Database integrity
    db_path = DB_PATH
    results["database"] = {"exists": db_path.exists(), "path": str(db_path)}
    
    if db_path.exists():
        try:
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row
            # Check tables
            tables = [r["name"] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
            results["database"]["tables"] = tables
            results["database"]["table_counts"] = {
                "indicators": conn.execute("SELECT COUNT(*) FROM indicators").fetchone()[0],
                "map_layers": conn.execute("SELECT COUNT(*) FROM map_layers").fetchone()[0],
                "datasets": conn.execute("SELECT COUNT(*) FROM datasets").fetchone()[0],
                "gamification": conn.execute("SELECT COUNT(*) FROM gamification").fetchone()[0],
            }
            # Check geometry column
            geom_count = conn.execute("SELECT COUNT(*) FROM map_layers WHERE geometry IS NOT NULL AND geometry != ''").fetchone()[0]
            results["database"]["layers_with_geometry"] = geom_count
            # Check indices
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
            # visit_count may not exist in older schemas
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
    
    # API endpoints - verify by querying the DB directly
    api_checks = {}
    for name, query in [
        ("indicators", "SELECT COUNT(*) FROM indicators"),
        ("datasets", "SELECT COUNT(*) FROM datasets"),
        ("map-layers", "SELECT COUNT(*) FROM map_layers"),
        ("gamification", "SELECT COUNT(*) FROM gamification"),
    ]:
        if conn:
            try:
                count = conn.execute(query).fetchone()[0]
                api_checks[name] = {"status": 200, "ok": True, "count": count}
            except Exception as e:
                api_checks[name] = {"status": "error", "error": str(e)}
    results["api_endpoints"] = api_checks
    
    # Map layer geometry validation
    map_checks = []
    if conn:
        try:
            rows = conn.execute("SELECT id, name, category, geometry FROM map_layers").fetchall()
            for r in rows:
                geom_valid = bool(r["geometry"]) and r["geometry"] != ""
                geom_type = ""
                if geom_valid:
                    try:
                        g = json.loads(r["geometry"])
                        geom_type = g.get("type", "")
                    except:
                        geom_type = "parse_error"
                map_checks.append({
                    "id": r["id"],
                    "name": r["name"],
                    "category": r["category"],
                    "geometry_valid": geom_valid,
                    "geometry_type_from_geojson": geom_type,
                })
        except Exception as e:
            map_checks = [{"error": str(e)}]
    results["map_layers"] = map_checks
    
    if conn:
        conn.close()
    
    # Overall status
    db_ok = results.get("database", {}).get("status") == "healthy"
    api_ok = all(v.get("ok", False) for v in api_checks.values())
    gam_ok = "status" not in results.get("gamification", {})
    map_ok = all(m.get("geometry_valid", False) for m in map_checks if isinstance(m, dict))
    
    results["overall"] = "healthy" if (db_ok and api_ok and gam_ok and map_ok) else "degraded"
    results["checks"] = {"database": db_ok, "api_endpoints": api_ok, "gamification": gam_ok, "map_layers": map_ok}
    
    return results


@app.get("/refresh")
@app.get("/diagnostics")
def diagnostics():
    """Full system diagnostics: DB integrity, API connectivity, gamification, map layers."""
    import json
    results = {}
    
    # Database integrity
    db_path = Path(__file__).parent / "data" / "volusia.db"
    results["database"] = {"exists": db_path.exists(), "path": str(db_path)}
    
    conn = None
    if db_path.exists():
        try:
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row
            # Check tables
            tables = [r["name"] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
            results["database"]["tables"] = tables
            results["database"]["table_counts"] = {
                "indicators": conn.execute("SELECT COUNT(*) FROM indicators").fetchone()[0],
                "map_layers": conn.execute("SELECT COUNT(*) FROM map_layers").fetchone()[0],
                "datasets": conn.execute("SELECT COUNT(*) FROM datasets").fetchone()[0],
                "gamification": conn.execute("SELECT COUNT(*) FROM gamification").fetchone()[0],
            }
            # Check geometry column
            geom_count = conn.execute("SELECT COUNT(*) FROM map_layers WHERE geometry IS NOT NULL AND geometry != ''").fetchone()[0]
            results["database"]["layers_with_geometry"] = geom_count
            # Check indices
            indices = [r["name"] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='index'").fetchall()]
            results["database"]["indices"] = indices
            results["database"]["status"] = "healthy"
        except Exception as e:
            results["database"]["status"] = "error"
            results["database"]["error"] = str(e)
    
    # Gamification state
    gamification_db = Path(__file__).parent / "data" / "volusia.db"
    if gamification_db.exists():
        try:
            conn = sqlite3.connect(str(gamification_db))
            conn.row_factory = sqlite3.Row
            gam_count = conn.execute("SELECT COUNT(*) FROM gamification").fetchone()[0]
            total_xp = conn.execute("SELECT SUM(total_xp) FROM gamification").fetchone()[0]
            avg_level = conn.execute("SELECT AVG(level) FROM gamification").fetchone()[0]
            # visit_count may not exist in older schemas
            try:
                total_visits = conn.execute("SELECT SUM(visit_count) FROM gamification").fetchone()[0]
            except sqlite3.OperationalError:
                total_visits = 0
            achievements = conn.execute("SELECT COUNT(*) FROM gamification WHERE achievements != '[]' AND achievements != ''").fetchone()[0]
            conn.close()
            results["gamification"] = {
                "users": gam_count,
                "total_xp": total_xp or 0,
                "avg_level": round(avg_level or 0, 1),
                "total_visits": total_visits or 0,
                "users_with_achievements": achievements,
            }
        except Exception as e:
            results["gamification"] = {"status": "error", "error": str(e)}
    
    # API endpoints - verify by querying the DB directly
    api_checks = {}
    try:
        indicator_count = conn.execute("SELECT COUNT(*) FROM indicators").fetchone()[0]
        api_checks["indicators"] = {"status": 200, "ok": True, "count": indicator_count}
    except Exception as e:
        api_checks["indicators"] = {"status": "error", "error": str(e)}
    try:
        dataset_count = conn.execute("SELECT COUNT(*) FROM datasets").fetchone()[0]
        api_checks["datasets"] = {"status": 200, "ok": True, "count": dataset_count}
    except Exception as e:
        api_checks["datasets"] = {"status": "error", "error": str(e)}
    try:
        layer_count = conn.execute("SELECT COUNT(*) FROM map_layers").fetchone()[0]
        api_checks["map-layers"] = {"status": 200, "ok": True, "count": layer_count}
    except Exception as e:
        api_checks["map-layers"] = {"status": "error", "error": str(e)}
    try:
        gam_count = conn.execute("SELECT COUNT(*) FROM gamification").fetchone()[0]
        api_checks["gamification"] = {"status": 200, "ok": True, "count": gam_count}
    except Exception as e:
        api_checks["gamification"] = {"status": "error", "error": str(e)}
    results["api_endpoints"] = api_checks
    
    # Map layer geometry validation
    map_checks = []
    if db_path.exists():
        try:
            conn = sqlite3.connect(str(db_path))
            rows = conn.execute("SELECT id, name, category, geometry FROM map_layers").fetchall()
            for r in rows:
                geom_valid = bool(r["geometry"]) and r["geometry"] != ""
                geom_type = ""
                if geom_valid:
                    try:
                        g = json.loads(r["geometry"])
                        geom_type = g.get("type", "")
                    except:
                        geom_type = "parse_error"
                map_checks.append({
                    "id": r["id"],
                    "name": r["name"],
                    "category": r["category"],
                    "geometry_valid": geom_valid,
                    "geometry_type_from_geojson": geom_type,
                })
            conn.close()
        except Exception as e:
            map_checks = [{"error": str(e)}]
    results["map_layers"] = map_checks
    
    # Overall status
    db_ok = results.get("database", {}).get("status") == "healthy"
    api_ok = all(v.get("ok", False) for v in api_checks.values())
    gam_ok = "status" not in results.get("gamification", {})
    map_ok = all(m.get("geometry_valid", False) for m in map_checks if isinstance(m, dict))
    
    if conn:
        conn.close()
    results["overall"] = "healthy" if (db_ok and api_ok and gam_ok and map_ok) else "degraded"
    results["checks"] = {"database": db_ok, "api_endpoints": api_ok, "gamification": gam_ok, "map_layers": map_ok}
    
    return results


def refresh():
    """Trigger a refresh pipeline run. Runs refresh_v2.py in-process."""
    import subprocess
    proc = subprocess.run(["python", str(Path(__file__).parent.parent / "scripts" / "refresh_v2.py")], capture_output=True, text=True, timeout=300)
    return {"status": "triggered", "stdout_tail": proc.stdout[-500:], "returncode": proc.returncode}

# Register gamification routes
get_gamification_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
