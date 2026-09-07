"""
Project Volusia — Static JSON Data Pipeline
Exports SQLite data to JSON files for static GitHub Pages deployment.
Run: python scripts/data_pipeline.py
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "data" / "volusia.db"
OUTPUT_DIR = Path(__file__).parent.parent / "data"

def export_json():
    """Export SQLite data to JSON files."""
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}")
        return
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    
    # Export all indicators
    cur = conn.execute("SELECT * FROM indicators ORDER BY category, name")
    indicators = [dict(r) for r in cur.fetchall()]
    with open(OUTPUT_DIR / "indicators.json", "w") as f:
        json.dump(indicators, f, indent=2)
    print(f"Exported {len(indicators)} indicators")
    
    # Export by category
    for cat in ["Economic", "Demographics", "Climate"]:
        cur = conn.execute("SELECT * FROM indicators WHERE category = ? ORDER BY name", (cat,))
        rows = [dict(r) for r in cur.fetchall()]
        fname = cat.lower() + ".json"
        with open(OUTPUT_DIR / fname, "w") as f:
            json.dump(rows, f, indent=2)
        print(f"Exported {len(rows)} {cat} indicators")
    
    # Export datasets
    cur = conn.execute("SELECT id, name, source, source_url, vintage FROM indicators ORDER BY id DESC LIMIT 50")
    datasets = [dict(r) for r in cur.fetchall()]
    with open(OUTPUT_DIR / "datasets.json", "w") as f:
        json.dump(datasets, f, indent=2)
    print(f"Exported {len(datasets)} datasets")
    
    # Export map layers
    try:
        cur = conn.execute("SELECT id, name, category, description, source, format FROM map_layers ORDER BY category, name")
        layers = [dict(r) for r in cur.fetchall()]
        with open(OUTPUT_DIR / "map-layers.json", "w") as f:
            json.dump(layers, f, indent=2)
        print(f"Exported {len(layers)} map layers")
    except Exception as e:
        print(f"Map layers export: {e}")
    
    # Export stakeholders
    stakeholders = [
        {"id": "business", "name": "Business Owners", "description": "Free market benchmarks, customer demographics, industry trends, pricing intelligence, and demand signals.", "icon": "\U0001f3ea", "highlights": ["Local market snapshot & competitor landscape", "Customer demographics & spending patterns", "Business formation & licensing data", "Quarterly economic briefings"]},
        {"id": "residents", "name": "Residents", "description": "Employment data, wage trends, cost-of-living metrics, school performance, health outcomes, and public spending.", "icon": "\U0001f3e0", "highlights": ["Employment & wage trends by sector", "Cost of living breakdown", "School & health data by area", "Open budget & public spending"]},
        {"id": "tourists", "name": "Tourists", "description": "Real-time conditions, honest reviews, local business availability, event calendars, and safety information.", "icon": "\U0001f3d6\ufe0f", "highlights": ["Real-time surf, weather & traffic", "Verified reviews & local availability", "Event calendars & booking", "Parking & transit information"]},
        {"id": "leaders", "name": "Leaders", "description": "Capital flow data, permitting velocity, infrastructure status, workforce availability, and demographic shifts.", "icon": "\U0001f4ca", "highlights": ["Capital flow & investment tracking", "Permitting & licensing velocity", "Workforce availability & wages", "Infrastructure capacity data"]}
    ]
    with open(OUTPUT_DIR / "stakeholders.json", "w") as f:
        json.dump(stakeholders, f, indent=2)
    print(f"Exported {len(stakeholders)} stakeholders")
    
    # Export news
    news = [
        {"id": "1", "title": "Project Volusia v2.0 Launched — Live Data Now Available", "summary": "Real economic, demographic, and climate indicators now live from Census, BLS, BEA, and NOAA.", "date": "2026-09-05", "category": "Platform"},
        {"id": "2", "title": "Q2 2026 Economic Briefing Published", "summary": "Unemployment at 4.6%, total employment at 189,265, per capita income at $59,259.", "date": "2026-08-15", "category": "Economic"},
        {"id": "3", "title": "New Climate Data Available", "summary": "NOAA annual climate summary: avg max temp 27.9°C, total precipitation 1,028mm.", "date": "2026-07-20", "category": "Climate"},
        {"id": "4", "title": "Population Growth Continues — 601,107 (2024)", "summary": "Volusia County adds ~9,000 residents year-over-year, reaching 601,107.", "date": "2026-06-30", "category": "Demographic"}
    ]
    with open(OUTPUT_DIR / "news.json", "w") as f:
        json.dump(news, f, indent=2)
    print(f"Exported {len(news)} news items")
    
    # Export health
    health = {
        "status": "healthy" if indicators else "degraded",
        "db_exists": True,
        "indicator_count": len(indicators),
        "categories": list(set(i["category"] for i in indicators)),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    with open(OUTPUT_DIR / "health.json", "w") as f:
        json.dump(health, f, indent=2)
    print("Exported health")
    
    conn.close()
    print("\nDone! All JSON files exported.")

if __name__ == "__main__":
    export_json()
