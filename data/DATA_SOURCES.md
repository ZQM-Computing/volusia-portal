# Project Volusia: Data Sources Registry

## Source Overview

All data in Project Volusia is sourced from public records, employer websites, job boards, and government databases. Each source is tracked with verification status.

## Primary Data Sources

### Employer Data

| Source | Type | Records | Status |
|--------|------|---------|--------|
| Employer websites | Direct | 151 | Verified |
| LinkedIn Company Pages | Professional Network | 89 | Verified |
| Florida Dept. of Economic Opportunity | Government | 45 | Verified |
| CareerSource Florida | Government | 38 | Verified |
| County/City official websites | Government | 28 | Verified |
| Chamber of Commerce directories | Association | 22 | Verified |
| Indeed employer profiles | Job Board | 18 | Verified |
| Glassdoor company profiles | Job Board | 12 | Verified |

### Job Postings

| Source | Type | Records | Status |
|--------|------|---------|--------|
| Employer career pages | Direct | 242 | Verified |
| Indeed.com | Job Board | 128 | Verified |
| LinkedIn Jobs | Professional Network | 96 | Verified |
| Government job boards | Government | 42 | Verified |
| CareerSource Florida | Government | 35 | Verified |
| ZipRecruiter | Job Board | 22 | Verified |
| Snagajob | Job Board | 18 | Verified |
| DirectEmployers | Job Board | 12 | Verified |

### Hiring Signals

| Source | Type | Records | Status |
|--------|------|---------|--------|
| Job board activity monitoring | Automated | 155 | Verified |
| Employer career page changes | Automated | 89 | Verified |
| LinkedIn hiring activity | Professional Network | 45 | Verified |
| News/media mentions | Media | 22 | Verified |
| Social media announcements | Social | 18 | Verified |
| Government labor reports | Government | 12 | Verified |

## Source Verification Protocol

### Confidence Levels

- **Confirmed**: Directly verified from employer or official source
- **Likely**: Multiple independent sources agree
- **Inferred**: Single source or indirect evidence

### Verification Checklist

- [ ] Source URL accessible and current
- [ ] Information matches employer's own claims
- [ ] Contact information verified (email bounces checked)
- [ ] Job posting still active (not expired)
- [ ] Pay range consistent with sector norms
- [ ] Location confirmed in Volusia County

## Data Collection Methodology

### Phase 1: Employer Identification
1. Query Florida Dept. of Economic Opportunity database
2. Cross-reference with CareerSource Florida listings
3. Search employer websites for Volusia County operations
4. Review Chamber of Commerce membership directories

### Phase 2: Job Posting Extraction
1. Scrape employer career pages (where permitted)
2. Aggregate from major job boards (Indeed, LinkedIn, etc.)
3. Collect from government job portals
4. Record pay ranges when publicly posted

### Phase 3: Hiring Signal Detection
1. Monitor job board activity for new postings
2. Track employer career page updates
3. Scan LinkedIn for hiring announcements
4. Review local news for expansion/layoff reports

### Phase 4: Verification
1. Cross-reference multiple sources for each data point
2. Verify contact information via email/phone testing
3. Confirm job posting currency (within 30 days)
4. Validate pay ranges against BLS data

## Data Quality Metrics

| Metric | Value |
|--------|-------|
| Total employers tracked | 151 |
| Employers with verified websites | 148 (98%) |
| Employers with direct contact info | 142 (94%) |
| Job postings with pay data | 187 (77%) |
| Hiring signals confirmed | 144 (93%) |
| Data freshness (avg days since update) | 7.2 |

## Source Limitations

- **Job boards**: May include duplicate postings across platforms
- **Employer websites**: Not all employers post jobs publicly
- **Government data**: Typically 30-90 day lag in reporting
- **Pay ranges**: Only ~77% of postings include compensation data
- **Small employers**: May have limited online presence

## Update Frequency

| Data Type | Update Cycle | Last Updated |
|-----------|--------------|--------------|
| Employer profiles | Weekly | 2026-09-07 |
| Job postings | Daily | 2026-09-07 |
| Hiring signals | Daily | 2026-09-07 |
| Contact verification | Monthly | 2026-09-01 |
| Full audit | Quarterly | 2026-07-01 |

## Contact & Contributions

To contribute new data or report inaccuracies:
1. Open a GitHub issue with source documentation
2. Include direct links to employer career pages
3. Provide screenshots of job postings (with dates)
4. Note any discrepancies found

---

*Last updated: September 7, 2026*
*Project Volusia v1.4*
