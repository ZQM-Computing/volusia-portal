# Project Volusia Data Dictionary
## Purpose
This document defines all data structures, fields, and relationships used in Project Volusia.

---

## Employers Table

|| Field | Type | Description |
|-------|------|-------------|
| `employer_id` | INTEGER | Primary key |
| `name` | TEXT | Legal employer name |
| `sector_id` | INTEGER | Foreign key to sectors |
| `city_id` | INTEGER | Foreign key to cities |
| `hq_in_volusia` | INTEGER | Headquarters located in Volusia (0/1) |
| `is_public` | INTEGER | Government/education/nonprofit (0/1) |
| `approx_employees` | INTEGER | Employee count estimate |
| `avg_annual_wage_override` | INTEGER | Wage override if known (nullable) |
| `description` | TEXT | Employer description |
| `keywords` | TEXT | Space-delimited search tokens |
| `website` | TEXT | Employer website URL |
| `source_verified_date` | TEXT | Last verification date (nullable) |
| `contact_email` | TEXT | HR/main contact email (nullable) |
| `contact_phone` | TEXT | Contact phone number (nullable) |
| `contact_notes` | TEXT | Special instructions for contact (nullable) |

### Contact Information
Contact fields are embedded within the employers table. 66 of 72 employers have verified contact information.

### Primary Source
`volusia_employers.db` (SQLite)

---

## Sectors Table

|| Field | Type | Description |
|-------|------|-------------|
| `sector_id` | INTEGER | Primary key |
| `name` | TEXT | Sector name |
| `color` | TEXT | Visual representation hex |

### Defined Sectors
1. Healthcare & Life Sciences
2. Education
3. Government & Public Safety
4. Aviation / Aerospace
5. Insurance & Financial Services
6. Manufacturing
7. Logistics & Distribution
8. Retail
9. Hospitality & Entertainment
10. Utilities & Infrastructure
11. Construction
12. Professional Services

---

## Cities Table

|| Field | Type | Description |
|-------|------|-------------|
| `city_id` | INTEGER | Primary key |
| `name` | TEXT | City name in Volusia County |
| `population_approx` | INTEGER | 2020 estimate |

### Key Cities
- Daytona Beach (72,000)
- DeLand (38,000)
- Port Orange (65,000)
- Deltona (90,000)
- New Smyrna Beach (32,000)
- Ormond Beach (45,000)
- Edgewater (25,000)
- Holly Hill (12,000)
- Orange City (15,000)
- DeLeon Springs (3,000)
- Crystal River (4,000)

---

## Jobs Table

|| Field | Type | Description |
|-------|------|-------------|
| `job_id` | INTEGER | Primary key |
| `employer_id` | INTEGER | Foreign key to employers |
| `title` | TEXT | Job title |
| `family` | TEXT | Job family/category (e.g., Nursing, Engineering) |
| `remote_eligible` | INTEGER | Remote work option (0/1) |
| `entry_level` | INTEGER | Entry-level position (0/1) |
| `posted_date` | TEXT | Application posting date |
| `url` | TEXT | Application URL |
| `source` | TEXT | Job board/source name |
| `pay_type` | TEXT | Pay structure (e.g., W2, Temp) |
| `pay_min` | INTEGER | Minimum pay amount |
| `pay_max` | INTEGER | Maximum pay amount |
| `pay_unit` | TEXT | Pay unit (e.g., 'hr', 'year') |
| `posted_ts` | TEXT | ISO timestamp when posted |
| `apply_url` | TEXT | Direct application URL |
| `cash_priority` | INTEGER | Priority score (0/1) |
| `notes` | TEXT | Additional job notes |
| `apply_email` | TEXT | Application email contact |
| `apply_phone` | TEXT | Application phone contact |
| `apply_notes` | TEXT | Instructions for applying |

---

## Applications Table

|| Field | Type | Description |
|-------|------|-------------|
| `app_id` | INTEGER | Primary key |
| `job_id` | INTEGER | Foreign key to jobs |
| `applied_on` | TEXT | Application date |
| `status` | TEXT | Application status |
| `notes` | TEXT | User notes |

---

## Hiring Signals Table

|| Field | Type | Description |
|-------|------|-------------|
| `signal_id` | INTEGER | Primary key |
| `employer_id` | INTEGER | Foreign key to employers |
| `signal_type` | TEXT | 'job_posting', 'tuition_program', 'market_tailwind', etc. |
| `source` | TEXT | Source URL |
| `date_seen` | TEXT | When signal was captured |
| `date_posted` | TEXT | Original posting date |
| `title` | TEXT | Signal title |
| `family` | TEXT | Category |
| `pay_min` | INTEGER | Minimum pay (nullable) |
| `pay_max` | INTEGER | Maximum pay (nullable) |
| `pay_unit` | TEXT | Pay unit (nullable) |
| `remote_eligible` | INTEGER | Remote option (0/1) |
| `entry_level` | INTEGER | Entry-level (0/1) |
| `cash_priority` | INTEGER | Priority score |
| `confidence` | TEXT | Verification confidence |
| `signal_tag` | TEXT | Classification tag |
| `notes` | TEXT | Additional info |
| `created_ts` | TEXT | Creation timestamp |
| `hiring_phase` | TEXT | Current hiring status |
| `contact_email` | TEXT | Contact email (nullable) |
| `contact_phone` | TEXT | Contact phone (nullable) |
| `contact_notes` | TEXT | Contact instructions (nullable) |

---

## Relationships Diagram

```
sectors ────────┐
  │             │
  ▼             ▼
employers ←── cities
  │
  ▼ (contact info embedded)
jobs ──► applications

employers ──► hiring_signals (43 signals for hiring trend analysis)
```

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Employers | 72 |
| Jobs | 29 |
| Hiring Signals | 43 |
| Sectors | 12 |
| Cities | 11 |

---

## Data Versioning

|| Version | Date | Changes |
|---------|------|---------|
| 1.2 | 2026-09-03 | Updated jobs table schema with pay_min/pay_max/pay_type/pay_unit fields |
| 1.1 | 2026-09-03 | Database/schema reconciliation |

---

*Data dictionary version 1.2*