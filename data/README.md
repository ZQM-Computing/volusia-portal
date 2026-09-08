# Data Directory

Economic intelligence data for Volusia County analysis.

## Key Files

### volusia_employers.db
SQLite database with 72 verified employers, 29 jobs, and 43 hiring signals.

### volusia_employers.sql
SQL dump file for database recreation.

### DATA_DICTIONARY.md
Documentation of all data fields and their meanings.

### DATA_SOURCES.md
Source verification and acquisition methods for each dataset.

### volusia_jobs_with_contacts.csv
Extended job data with contact information (25 unique employers from CSV cross-reference).

## Schema

```
sectors ────────┐
  │             │
  ▼             ▼
employers ←── cities
  │
  ├── employers_contacts (1-1 relationship)
  │
  ▼
jobs
  │
  ▼
applications

employers ─┬─ jobs
           └─ hiring_signals (1-N: multiple signals per employer over time)
```

## Data Quality

All employer data has been verified through:
- Official company websites
- State employment databases
- LinkedIn company pages
- Press release validation
- Job board scraping (hiring_signals)

Last updated: 2026-09-03

## Data Volume

| Entity | Count |
|--------|-------|
| Employers | 72 |
| Employer Contacts | 66 |
| Jobs | 29 |
| Hiring Signals | 43 |
| Sectors | 12 |
| Cities | 11 |