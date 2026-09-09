# API Keys Required

The following API keys are needed for full data coverage. Currently all are unset.

| Source | Key Env Var | Endpoint | Notes |
|--------|------------|----------|-------|
| Census | `CENSUS_API_KEY` | data.census.gov | Works without key for some endpoints |
| BLS | `BLS_API_KEY` | bls.gov | Required for employment data |
| BEA | `BEA_API_KEY` | bea.gov | Required for personal income data |
| NOAA | `NOAA_API_KEY` | ncei.noaa.gov | Optional for climate data |
| Redfin | `REDFIN_API_KEY` | redfin.com | Optional for housing data |
| Zillow | `ZILLOW_API_KEY` | zillow.com | Optional for housing data |
| C2ER | `C2ER_API_KEY` | c2er.org | Optional for cost of living |
| FRED | `FRED_API_KEY` | fred.stlouisfed.org | Optional for economic data |
| CVB | `CVB_API_KEY` | daytonabeach.com | Optional for hotel data |

## Setup

Set environment variables in the Docker compose file or the host system:
```bash
export CENSUS_API_KEY=your_key
export BLS_API_KEY=your_key
export BEA_API_KEY=your_key
```

Then restart the backend container:
```bash
docker compose down && docker compose up -d
```
