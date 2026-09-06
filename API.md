# API Documentation — Project Volusia

> Complete reference for all API endpoints.

---

## Portal API (port 8789)

### Health & Status

#### `GET /api/health`

Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "service": "project-volusia",
  "indicators": 474,
  "sources": 112,
  "uptime_seconds": 3600
}
```

#### `GET /api/status`

Detailed system status.

**Response**:
```json
{
  "status": "operational",
  "indicators": 474,
  "categories": 15,
  "sources": 112,
  "submissions": 21,
  "quality_score": 96.8,
  "sla": {
    "uptime": "99.9%",
    "response_time": "<200ms",
    "freshness": "95%"
  },
  "endpoints": {
    "total": 15,
    "operational": 15
  },
  "services": {
    "portal": "running",
    "contribution_api": "running",
    "proxy": "running"
  }
}
```

### Indicators

#### `GET /api/indicators`

List all indicators.

**Query Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| category | string | Filter by category |
| source | string | Filter by source |
| search | string | Search by name/description |

**Response**:
```json
[
  {
    "name": "total_population_pep_2024",
    "value": "601107",
    "unit": "people",
    "category": "Demographics",
    "source": "Census PEP",
    "source_url": "https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/counties/totals/co-est2025-alldata.csv",
    "vintage": "2024",
    "description": "Total population 2024 from Census Population Estimates Program"
  }
]
```

#### `GET /api/indicators/{name}`

Get a specific indicator.

**Response**:
```json
{
  "name": "total_population_pep_2024",
  "value": "601107",
  "unit": "people",
  "category": "Demographics",
  "source": "Census PEP",
  "source_url": "https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/counties/totals/co-est2025-alldata.csv",
  "vintage": "2024",
  "description": "Total population 2024 from Census Population Estimates Program"
}
```

### Charts

#### `GET /api/chart/population_trend.png`

Population trend line chart.

**Response**: PNG image (~19KB)

#### `GET /api/chart/employment_overview.png`

Employment overview bar chart.

**Response**: PNG image (~21KB)

#### `GET /api/chart/climate_summary.png`

Climate summary bar chart.

**Response**: PNG image (~21KB)

#### `GET /api/chart/unemployment_trend.png`

Unemployment trend line chart.

**Response**: PNG image (~16KB)

#### `GET /api/chart/wage_trend.png`

Wage trend line chart.

**Response**: PNG image (~18KB)

#### `GET /api/chart/income_overview.png`

Income overview bar chart.

**Response**: PNG image (~20KB)

#### `GET /api/chart/housing_overview.png`

Housing overview bar chart.

**Response**: PNG image (~22KB)

#### `GET /api/chart/demographics.png`

Demographics bar chart.

**Response**: PNG image (~25KB)

#### `GET /api/chart/education_health.png`

Education and health bar chart.

**Response**: PNG image (~23KB)

#### `GET /api/chart/traffic_overview.png`

Traffic overview bar chart.

**Response**: PNG image (~20KB)

#### `GET /api/chart/schools_by_type.png`

Schools by type bar chart.

**Response**: PNG image (~18KB)

#### `GET /api/chart/infrastructure.png`

Infrastructure bar chart.

**Response**: PNG image (~24KB)

### Analysis

#### `GET /api/search?q={query}&category={cat}&source={src}&limit={n}`

Search indicators.

**Query Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| q | string | Search query |
| category | string | Filter by category |
| source | string | Filter by source |
| limit | integer | Max results (default: 50) |

**Response**:
```json
{
  "query": "population",
  "results": [
    {
      "name": "total_population_pep_2024",
      "value": "601107",
      "unit": "people",
      "category": "Demographics"
    }
  ],
  "total": 1
}
```

#### `GET /api/compare?name1={name}&name2={name}`

Compare two indicators side by side.

**Query Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| name1 | string | First indicator name |
| name2 | string | Second indicator name |

**Response**:
```json
{
  "indicator1": {
    "name": "total_population_pep_2024",
    "value": "601107",
    "unit": "people"
  },
  "indicator2": {
    "name": "population_2025_estimate",
    "value": "606573",
    "unit": "people"
  }
}
```

#### `GET /api/trend?name={name}`

Get trend data for an indicator.

**Query Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| name | string | Indicator name |

**Response**:
```json
{
  "name": "total_population_pep_2024",
  "data": [
    {"value": 580529, "vintage": "2022"},
    {"value": 591936, "vintage": "2023"},
    {"value": 601107, "vintage": "2024"}
  ]
}
```

#### `GET /api/correlation`

Get cross-category correlation data.

**Response**:
```json
{
  "population_vs_income": 0.85,
  "employment_vs_wages": 0.72,
  "education_vs_health": 0.68
}
```

### Export

#### `GET /api/export/csv`

Download all indicators as CSV.

**Response**: CSV file

#### `GET /api/export/json`

Download all indicators as JSON.

**Response**: JSON file

#### `GET /api/export/full?format=json|csv`

Full data export with metadata.

**Query Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| format | string | Export format (json or csv) |

**Response**:
```json
{
  "metadata": {
    "generated_at": "2026-09-06T02:00:00+00:00",
    "total_indicators": 474,
    "total_sources": 112,
    "quality_score": 96.8
  },
  "indicators": [...]
}
```

### Citations

#### `GET /api/citations`

Get citation validation report.

**Response**:
```json
{
  "total": 474,
  "average_score": 95.6,
  "citations": [
    {
      "indicator": "total_population_pep_2024",
      "source": "Census PEP",
      "url": "https://www2.census.gov/...",
      "vintage": "2024",
      "score": 100,
      "issues": []
    }
  ]
}
```

### Coherence

#### `GET /api/coherence`

Get cross-source disagreement groups.

**Response**:
```json
{
  "groups": [
    {
      "name": "population",
      "sources": [
        {"name": "Census PEP", "value": 601107},
        {"name": "Census ACS", "value": 606573}
      ],
      "difference_pct": 0.9
    }
  ]
}
```

### Datasets

#### `GET /api/datasets`

Get dataset history.

**Response**:
```json
[
  {
    "id": 1,
    "name": "census_pep_2024",
    "source": "Census PEP",
    "vintage": "2024",
    "indicators_count": 3,
    "created_at": "2026-09-05T01:00:00+00:00"
  }
]
```

### Executive Summary

#### `GET /api/executive-summary`

Get key metrics and freshness status.

**Response**:
```json
{
  "population": {
    "value": 601107,
    "unit": "people",
    "source": "Census PEP",
    "vintage": "2024",
    "freshness": "current"
  },
  "unemployment": {
    "value": 5.3,
    "unit": "%",
    "source": "BLS LAUS",
    "vintage": "2026-07",
    "freshness": "current"
  },
  "median_income": {
    "value": 70044,
    "unit": "$",
    "source": "Census ACS",
    "vintage": "2020-2024",
    "freshness": "current"
  }
}
```

---

## Contribution API (port 8790)

### Submit Contribution

#### `POST /api/v1/contributions`

Submit a new contribution.

**Request Body**:
```json
{
  "contribution_type": "data_source",
  "content": {
    "title": "New Census Data Source",
    "description": "ACS 5-year estimates for Volusia County",
    "source_url": "https://data.census.gov/table/ACSDP5Y2024.DP05",
    "source_agency": "Census ACS",
    "category": "Demographics",
    "vintage": "2024",
    "indicators": [
      {"name": "median_age", "value": "47.3", "unit": "years"}
    ]
  }
}
```

**Response** (`201 Created`):
```json
{
  "submission_id": "SUB-DATA_SOURCE-20260906082823811456",
  "status": "queued",
  "reviewer": "Node-3 (Data Pipeline)",
  "estimated_review": "3 business days"
}
```

### List Contributions

#### `GET /api/v1/contributions`

List all contributions.

**Query Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| status | string | Filter by status (queued, approved, rejected) |
| type | string | Filter by contribution type |
| limit | integer | Max results (default: 50) |

**Response**:
```json
[
  {
    "submission_id": "SUB-DATA_SOURCE-20260906082823811456",
    "contribution_type": "data_source",
    "status": "queued",
    "created_at": "2026-09-06T08:28:23+00:00"
  }
]
```

### Get Contribution

#### `GET /api/v1/contributions/{submission_id}`

Get a specific contribution.

**Response**:
```json
{
  "submission_id": "SUB-DATA_SOURCE-20260906082823811456",
  "contribution_type": "data_source",
  "content": {...},
  "status": "queued",
  "reviewer": "Node-3 (Data Pipeline)",
  "created_at": "2026-09-06T08:28:23+00:00"
}
```

### Update Contribution

#### `PATCH /api/v1/contributions/{submission_id}`

Update contribution status.

**Request Body**:
```json
{
  "status": "approved",
  "notes": "Source verified and data integrated"
}
```

**Response**:
```json
{
  "submission_id": "SUB-DATA_SOURCE-20260906082823811456",
  "status": "approved",
  "updated_at": "2026-09-06T09:00:00+00:00"
}
```

### Health

#### `GET /api/v1/health`

Contribution API health check.

**Response**:
```json
{
  "status": "healthy",
  "service": "project-vulusia-contributions",
  "version": "2.0"
}
```

---

## HTML Pages

| URL | Description |
|-----|-------------|
| `/` | Main website |
| `/contribute/` | Contribution landing page |
| `/project-volusia` | Portal with live data |
| `/data-explorer` | Filterable data table |
| `/dashboard` | Executive dashboard |
| `/sensors` | Real-time sensors and cameras |
| `/osint-recon` | OSINT sources |
| `/osint-report` | OSINT recon report |
| `/geoint` | GEOINT surface |
| `/citations` | Citation validation |

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request (invalid data) |
| 401 | Unauthorized (invalid API key) |
| 404 | Not found |
| 500 | Internal server error |

---

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| Read endpoints | 1000/hour |
| Write endpoints | 100/hour |
| Chart generation | 50/hour |

---

## Examples

### cURL

```bash
# Health check
curl http://localhost:80/api/health

# List indicators
curl http://localhost:80/api/indicators

# Search
curl "http://localhost:80/api/search?q=population"

# Submit contribution
curl -X POST http://localhost:80/api/v1/contributions \
  -H "Content-Type: application/json" \
  -d '{"contribution_type":"tool","content":{"title":"My Tool"}}'
```

### Python

```python
import requests

# Get indicators
r = requests.get("http://localhost:80/api/indicators")
data = r.json()

# Submit contribution
r = requests.post("http://localhost:80/api/v1/contributions", json={
    "contribution_type": "data_source",
    "content": {
        "title": "New Source",
        "source_url": "https://example.gov/data",
        "category": "Economy"
    }
})
print(r.json())
```

### JavaScript

```javascript
// Get indicators
const r = await fetch('http://localhost:80/api/indicators');
const data = await r.json();

// Submit contribution
const r = await fetch('http://localhost:80/api/v1/contributions', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        contribution_type: 'data_source',
        content: {title: 'New Source'}
    })
});
```

---

*Last updated: 2026-09-06*
