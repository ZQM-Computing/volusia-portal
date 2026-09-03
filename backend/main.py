"""
Project Volusia — FastAPI Backend
Serves real economic indicators from scraped data.
"""

import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from scraper import (
    scrape_census_dp03,
    scrape_census_dp05,
    scrape_noaa_daily,
    scrape_open_meteo_forecast,
    scrape_redfin_volusia,
    scrape_volusia_business,
    scrape_zillow_metro_zhvi,
)

app = FastAPI(title="Project Volusia API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CACHE_DIR = Path(__file__).parent.parent / "data" / "cache"


def load_json(name: str) -> Optional[dict]:
    path = CACHE_DIR / f"{name}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


@app.get("/")
def root():
    return {"service": "Project Volusia API", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/indicators")
def get_all_indicators():
    """Return all available indicators from cached scraper data."""
    indicators = {}

    # Census DP03 - Economic
    census_econ = load_json("census_dp03")
    if census_econ:
        indicators["census_economic"] = census_econ

    # Census DP05 - Demographics
    census_demo = load_json("census_dp05")
    if census_demo:
        indicators["census_demographics"] = census_demo

    # NOAA Weather
    noaa = load_json("noaa_daily_2025-09-02_2026-09-02")
    if noaa:
        indicators["noaa_weather"] = noaa

    # Open-Meteo Forecast
    open_meteo = load_json("open_meteo_forecast")
    if open_meteo:
        indicators["weather_forecast"] = open_meteo

    # Redfin Housing
    redfin = load_json("redfin_volusia")
    if redfin:
        indicators["housing_market"] = redfin

    # Volusia Business
    volusia_biz = load_json("volusia_business")
    if volusia_biz:
        indicators["economy"] = volusia_biz

    # Zillow ZHVI
    zillow = load_json("zillow_zhvi")
    if zillow:
        indicators["zillow_home_value"] = zillow

    return indicators


@app.get("/indicators/economic")
def get_economic():
    """Return economic indicators (income, employment, poverty)."""
    result = {}

    census = load_json("census_dp03")
    if census:
        result["medianHouseholdIncome"] = census.get("medianHouseholdIncome")
        result["unemploymentRate"] = census.get("unemploymentRate")
        result["povertyRate"] = census.get("povertyRate")
        result["perCapitaIncome"] = census.get("perCapitaIncome")
        result["commuteTimeMinutes"] = census.get("commuteTimeMinutes")
        result["source"] = census.get("source")
        result["vintage"] = census.get("vintage")

    volusia_biz = load_json("volusia_business")
    if volusia_biz:
        result["gdp"] = volusia_biz.get("gdp")
        result["gdpRank"] = volusia_biz.get("gdpRank")

    return result


@app.get("/indicators/demographics")
def get_demographics():
    """Return demographic indicators."""
    census = load_json("census_dp05")
    if not census:
        raise HTTPException(status_code=404, detail="Demographic data not available")
    return census


@app.get("/indicators/housing")
def get_housing():
    """Return housing market indicators."""
    redfin = load_json("redfin_volusia")
    zillow = load_json("zillow_zhvi")

    result = {}
    if redfin:
        result["medianSalePrice"] = redfin.get("medianSalePrice")
        result["yoyPriceChange"] = redfin.get("yoyPriceChange")
        result["redfinSource"] = redfin.get("source")
    if zillow:
        result["zillowHomeValue"] = zillow.get("medianHomeValue")
        result["zillowYoyChange"] = zillow.get("yoyChange")

    if not result:
        raise HTTPException(status_code=404, detail="Housing data not available")
    return result


@app.get("/indicators/weather")
def get_weather():
    """Return current weather and forecast."""
    open_meteo = load_json("open_meteo_forecast")
    noaa = load_json("noaa_daily_2025-09-02_2026-09-02")

    result = {}
    if open_meteo:
        result["current"] = open_meteo.get("current")
        result["forecast"] = open_meteo.get("forecast")
    if noaa:
        result["station"] = noaa.get("station")
        result["stationName"] = noaa.get("stationName")

    if not result:
        raise HTTPException(status_code=404, detail="Weather data not available")
    return result


@app.post("/refresh")
def refresh_data():
    """Trigger a refresh of all scraper data."""
    results = {}

    try:
        results["census_dp03"] = scrape_census_dp03()
    except Exception as e:
        results["census_dp03"] = {"error": str(e)}

    try:
        results["census_dp05"] = scrape_census_dp05()
    except Exception as e:
        results["census_dp05"] = {"error": str(e)}

    try:
        results["noaa_daily"] = scrape_noaa_daily()
    except Exception as e:
        results["noaa_daily"] = {"error": str(e)}

    try:
        results["open_meteo"] = scrape_open_meteo_forecast()
    except Exception as e:
        results["open_meteo"] = {"error": str(e)}

    try:
        results["redfin"] = scrape_redfin_volusia()
    except Exception as e:
        results["redfin"] = {"error": str(e)}

    try:
        results["volusia_business"] = scrape_volusia_business()
    except Exception as e:
        results["volusia_business"] = {"error": str(e)}

    try:
        results["zillow_zhvi"] = scrape_zillow_metro_zhvi()
    except Exception as e:
        results["zillow_zhvi"] = {"error": str(e)}

    return {"status": "refresh complete", "results": {k: "OK" if v and "error" not in v else "FAILED" for k, v in results.items()}}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
