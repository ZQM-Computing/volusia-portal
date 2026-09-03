"""
Project Volusia — FastAPI Backend
Serves real economic indicators from SQLite database.
"""

import sqlite3
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Project Volusia API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = Path(__file__).parent.parent / "data" / "volusia.db"


def _db_rows(query, params=()):
    if not DB_PATH.exists():
        return []
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.execute(query, params)
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


@app.get("/")
def root():
    return {"service": "Project Volusia API", "version": "2.0.0"}


@app.get("/health")
def health():
    db_exists = DB_PATH.exists()
    indicator_count = 0
    if db_exists:
        conn = sqlite3.connect(str(DB_PATH))
        try:
            indicator_count = conn.execute("SELECT COUNT(*) FROM indicators").fetchone()[0]
        finally:
            conn.close()
    return {
        "status": "healthy" if db_exists and indicator_count > 0 else "degraded",
        "db_exists": db_exists,
        "indicator_count": indicator_count,
    }


@app.get("/indicators")
def get_all_indicators():
    rows = _db_rows("SELECT * FROM indicators ORDER BY category, name")
    return {"count": len(rows), "indicators": rows}


@app.get("/indicators/economic")
def get_economic():
    rows = _db_rows("SELECT * FROM indicators WHERE category = 'Economic' ORDER BY name")
    return {"count": len(rows), "indicators": rows}


@app.get("/indicators/demographics")
def get_demographics():
    rows = _db_rows("SELECT * FROM indicators WHERE category = 'Demographics' ORDER BY name")
    return {"count": len(rows), "indicators": rows}


@app.get("/indicators/climate")
def get_climate():
    rows = _db_rows("SELECT * FROM indicators WHERE category = 'Climate' ORDER BY name")
    return {"count": len(rows), "indicators": rows}


@app.get("/datasets")
def get_datasets():
    rows = _db_rows("SELECT id, name, source, source_url, access_date, vintage FROM datasets ORDER BY id DESC LIMIT 50")
    return {"count": len(rows), "datasets": rows}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
