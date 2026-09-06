"""Project Volusia — FastAPI Backend v3
Serves real economic indicators from SQLite database + CSV downloads.
"""
import csv, io, os, sqlite3
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
    rows = _db_rows("SELECT id, name, category, description, source, format, url FROM map_layers ORDER BY category, name")
    return {"count": len(rows), "layers": rows}

@app.get("/refresh")
def refresh():
    """Trigger a refresh pipeline run. Runs refresh_v2.py in-process."""
    import subprocess
    proc = subprocess.run(["python", str(Path(__file__).parent.parent / "scripts" / "refresh_v2.py")], capture_output=True, text=True, timeout=300)
    return {"status": "triggered", "stdout_tail": proc.stdout[-500:], "returncode": proc.returncode}

# Register gamification routes
get_gamification_routes(app)

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
