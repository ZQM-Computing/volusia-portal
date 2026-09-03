"""
Project Volusia — FastAPI Backend
Serves real economic indicators from cached data.
"""

import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Project Volusia API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CACHE_DIR = Path(__file__).parent.parent / "data" / "cache"


def load_json(name: str) -> dict:
    path = CACHE_DIR / f"{name}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Data not found: {name}")
    return json.loads(path.read_text())


@app.get("/")
def root():
    return {"service": "Project Volusia API", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/indicators")
def get_all_indicators():
    """Return all available indicators."""
    indicators = {}
    for name in ["census_dp03", "census_dp05", "bls_laus", "bea_income"]:
        try:
            indicators[name] = load_json(name)
        except HTTPException:
            indicators[name] = {"error": "Data not available"}
    return indicators


@app.get("/indicators/economic")
def get_economic():
    """Return economic indicators (income, employment, poverty)."""
    return {
        "acs_economic": load_json("census_dp03"),
        "bls_unemployment": load_json("bls_laus"),
    }


@app.get("/indicators/demographics")
def get_demographics():
    """Return demographic indicators."""
    return load_json("census_dp05")


@app.get("/indicators/income")
def get_income():
    """Return income indicators."""
    return {
        "acs_income": load_json("census_dp03"),
        "bea_personal_income": load_json("bea_income"),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
