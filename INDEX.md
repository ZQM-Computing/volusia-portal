# Project Volusia: Complete Index

## Directory Navigation

### Mission Statement/
Documents establishing project philosophy and approach

| File | Purpose |
|------|---------|
| MISSION_STATEMENT.md | Project vision and scope |
| AGENTIC_CONTRIBUTION_STRATEGY.md | AI-human collaboration methodology |
| GUIDING_PRINCIPLES_VOLUSIA_COUNTY.md | Core operational principles |
| OPEN_INTELLIGENCE_DATA_DRIVEN_CHARTER.md | Intelligence infrastructure charter |

### Data/
All data definitions and source documentation

| File | Purpose |
|------|---------|
| volusia_employers.sql | SQL database schema + employer records |
| volusia_employers.db | Compiled SQLite database |
| volusia_jobs_with_contacts.csv | Job listings with contact info |
| DATA_DICTIONARY.md | Complete field definitions for all tables |
| DATA_SOURCES.md | Source registry with verification status |

### Methodology/
Process documentation and standards

| File | Purpose |
|------|---------|
| EMPLOYER_PROFILE_TEMPLATE.md | Standard format for employer entries |
| EROSION_MANAGEMENT_FRAMEWORK.md | Economic decline detection/intervention |
| SECTOR_CLASSIFICATION_SCHEME.md | NAICS-based sector definitions |
| AGENTIC_CONTRIBUTION_STRATEGY.md | AI-assisted contribution workflow |
| ECONOMIC_PROJECTION_MODEL.md | Statistical forecasting methodology |

### Report/
Comprehensive analysis and outputs

| File | Purpose |
|------|---------|
| COMPREHENSIVE_REPORT.md | Full economic landscape analysis |
| STAKEHOLDER_ENGAGEMENT_PLAN.md | Outreach strategy and timeline |
| README.md | Project overview and quick start |

### Report/EMPLOYERS/
Individual employer profiles (151 created)

| File Count | Description |
|------------|-------------|
| 151 profiles | Complete employer database profiles with jobs |
| Directory | Report/EMPLOYERS/*.md |
| Schema | Automated from volusia_employers.db |

### Tools/
Operational utilities and checklists

| File | Purpose |
|------|---------|
| DATA_VERIFICATION_CHECKLIST.md | Source verification protocol |
| verify_data.py | Automated data verification script |

---

## Key Data Summary

### Employers: 151 total across 17 sectors and 17 cities
- Manufacturing: 24 employers
- Healthcare & Life Sciences: 22 employers
- Government & Public Safety: 18 employers
- Hospitality & Entertainment: 17 employers
- Retail: 12 employers
- Education: 8 employers
- Insurance & Financial Services: 8 employers
- Non-profit & Community: 8 employers
- Aviation / Aerospace: 6 employers
- Logistics & Distribution: 6 employers
- Arts, Culture & Recreation: 5 employers
- Professional Services: 5 employers
- Construction: 4 employers
- Utilities & Infrastructure: 3 employers
- Agriculture & Food Production: 2 employers
- Technology & IT: 2 employers
- Real Estate & Development: 1 employer

### Jobs: 242 open positions across all employers
- Healthcare & Life Sciences: 46 positions
- Hospitality & Entertainment: 41 positions
- Government & Public Safety: 28 positions
- Manufacturing: 25 positions
- Retail: 21 positions
- Education: 13 positions
- Insurance & Financial Services: 13 positions
- Professional Services: 11 positions
- Logistics & Distribution: 10 positions
- Non-profit & Community: 8 positions
- Aviation / Aerospace: 7 positions
- Arts, Culture & Recreation: 5 positions
- Utilities & Infrastructure: 5 positions
- Construction: 4 positions
- Agriculture & Food Production: 2 positions
- Technology & IT: 2 positions
- Real Estate & Development: 1 position

### Hiring Signals: 155 tracked signals
- Confirmed: 144 signals
- Likely: 9 signals
- Inferred: 2 signals
- Date range: 2026-07-20 to 2026-09-01

### Cities: 17 Volusia County cities covered
- Daytona Beach: 53 employers
- DeLand: 29 employers
- Edgewater: 11 employers
- New Smyrna Beach: 9 employers
- Deltona: 8 employers
- Ormond Beach: 6 employers
- Port Orange: 6 employers
- DeBary: 5 employers
- Orange City: 5 employers
- Oak Hill: 4 employers
- South Daytona: 4 employers
- Lake Helen: 3 employers
- Pierson: 3 employers
- Ponce Inlet: 3 employers
- DeLeon Springs: 1 employer
- Holly Hill: 1 employer
- Crystal River: 0 employers (placeholder)

---

## Quick Reference

### For Employers
1. Check `Data/DATA_DICTIONARY.md` for field definitions
2. Use `Methodology/EMPLOYER_PROFILE_TEMPLATE.md` for new entries
3. Verify with `Tools/DATA_VERIFICATION_CHECKLIST.md`

### For Researchers
1. Start with `Report/COMPREHENSIVE_REPORT.md`
2. Review `Data/DATA_SOURCES.md` for provenance
3. Check individual profiles in `Report/EMPLOYERS/`

### For Contributors
1. Read `MISSION_STATEMENT.md`
2. Follow `Methodology/AGENTIC_CONTRIBUTION_STRATEGY.md`
3. Use verification checklist before submitting

### For Stakeholders
1. See `Report/STAKEHOLDER_ENGAGEMENT_PLAN.md`
2. Contact via GitHub issues or project lead

---

## Data Files

### Primary Data
- `Data/volusia_employers.db` - Main employer database (SQLite)
- `Data/volusia_employers.sql` - SQL schema + data dump
- `Data/volusia_jobs_with_contacts.csv` - Job listings with contact info

### Generated Artifacts
- `Report/EMPLOYERS/*.md` - 151 individual employer profiles
- `Tools/verify_data.py` - Data verification script

---

## Technical Verification

Run the verification script to validate all data:

```bash
python Tools/verify_data.py
```

Expected output:
- 151 employers verified
- All job records linked to valid employers
- All sector references valid
- All city references valid
- 242 job postings across 151 employers
- 155 hiring signals tracked

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-09-02 | Initial release: MISSION, DATA, METHODOLOGY, REPORT |
| 1.1 | 2026-09-03 | Added 5 employer profiles, data files |
| 1.2 | 2026-09-03 | Updated to reflect actual counts (72 employers), generated 72 employer profiles |
| 1.3 | 2026-09-07 | Added 34 new employers (106 total), 109 jobs, 50 hiring signals. New sectors: Professional Services, Hospitality |
| 1.4 | 2026-09-07 | Added 45 new employers (151 total), 242 jobs, 155 hiring signals. New sectors: Technology & IT, Non-profit & Community, Arts Culture & Recreation, Real Estate & Development, Agriculture & Food Production. Added 6 new cities: DeBary, South Daytona, Ponce Inlet, Lake Helen, Pierson, Oak Hill. All employers now have at least 1 job posting. |

---

*Last updated: September 7, 2026*
*This documentation represents Project Volusia v1.4*
