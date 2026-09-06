# PHASE 1 FOUNDATION — OPERATIONS & VERIFICATION LAYER
# Project Volusia — Living Document
# Date: 2026-09-03 | Version: 1.0
# Classification: Internal — Execution & Accountability
#
# This document is the operational spine for Phase 1. It tracks what was
# CLAIMED vs. what is ACTUAL, logs decisions, monitors system health,
# and provides the missing templates referenced across the charter corpus.

---

## 0. DOCUMENT PURPOSE

The existing charter documents define what Project Volusia believes and intends.
This document defines how we verify, track, and execute against those intentions.

Without this layer, charters become shelf documents. With it, every claim in every
charter can be tested against reality.

---

## 1. VERIFIED VS. CLAIMED SCORECARD

### 1.1 DATA SOURCE ACCESS — CLAIMED vs. ACTUAL

| SOURCE | CLAIMED ACCESS | ACTUAL STATUS | VERIFIED DATE | VERIFIED BY |
|--------|---------------|---------------|---------------|-------------|
| Census ACS 5-Year (DP03/DP05) | API, no key | REQUIRES KEY (302 redirect) | 2026-09-03 | ZQM Labs |
| Census PEP | Not mentioned in charters | WORKS (no key) | 2026-09-03 | ZQM Labs |
| BLS LAUS | API, no key | REQUIRES KEY (403) | 2026-09-03 | ZQM Labs |
| BLS QCEW | CSV download | WORKS (no key) | 2026-09-03 | ZQM Labs |
| BEA Regional (CAINC1) | API, no key | REQUIRES KEY | 2026-09-03 | ZQM Labs |
| NOAA NCEI | Not in charters | WORKS (no key) | 2026-09-03 | ZQM Labs |
| Zillow ZHVI/ZORI | Direct download | PATH CHANGED (404) | 2026-09-03 | ZQM Labs |
| Realtor.com | County-level data | NATIONAL ONLY | 2026-09-03 | ZQM Labs |
| Volusia Property Appraiser | Public parcel data | TIMEOUT (blocks bots) | 2026-09-03 | ZQM Labs |
| FDOT Traffic | Direct download | 404 (site restructured) | 2026-09-03 | ZQM Labs |
| VOTRAN Ridership | PDF reports | 404 | 2026-09-03 | ZQM Labs |
| FCC Broadband Map | API access | 403 (browser only) | 2026-09-03 | ZQM Labs |
| STR Hotel Data | Summary reports public | GATED (paid sub) | 2026-09-03 | ZQM Labs |
| FEMA Flood Maps | API search | 404 (endpoint changed) | 2026-09-03 | ZQM Labs |
| CDC PLACES | API | 404 | 2026-09-03 | ZQM Labs |
| FL DOH CHARTS | Direct access | 302 redirect | 2026-09-03 | ZQM Labs |
| County Health Rankings | API | 404 | 2026-09-03 | ZQM Labs |
| FL School Report Cards | Direct download | 403 | 2026-09-03 | ZQM Labs |
| Volusia County ACFR | PDF on site | 200 (found in nav) | 2026-09-03 | ZQM Labs |
| USGS Water Data | Direct API | 301 redirect | 2026-09-03 | ZQM Labs |

**Summary:** Of 20 sources tested, 3 work as claimed (15%), 4 need free API keys (20%),
4 are blocked/restructured (20%), 9 are missing/gated/inaccessible (45%).

### 1.2 TOOL STATUS — CLAIMED vs. ACTUAL

| TOOL | CLAIMED STATUS | ACTUAL STATUS | NOTES |
|------|---------------|---------------|-------|
| Census API Wrapper | Built, functional | BLOCKED (no key) | Code exists, API rejects |
| BLS Scraper | Built, functional | BLOCKED (no key) | Code exists, API rejects |
| BLS QCEW Fetcher | Built, functional | WORKS | Real data produced |
| BEA Fetcher | Built, functional | BLOCKED (no key) | Code exists, API rejects |
| NOAA Fetcher | Built, functional | WORKS | Real data produced |
| PEP Fetcher | Built, functional | BLOCKED (no key) | Code exists, API rejects |
| FastAPI Portal | Built, functional | WORKS | Running on localhost:8000 |
| SQLite DB Layer | Built, functional | WORKS | 3 tables, audit trail |
| refresh.py Pipeline | Built, functional | PARTIAL | 2/6 fetchers work |

### 1.3 CHARTER CLAIMS — VERIFICATION STATUS

| CLAIM | SOURCE DOC | VERIFICATION | STATUS |
|-------|-----------|--------------|--------|
| "100% of business-critical data available via governed API" | MISSION_STATEMENT.md | No data is served via API yet | NOT MET |
| "Sub-second analytics on core business events" | MISSION_STATEMENT.md | Portal serves static indicators | NOT MET |
| "Open developer portal with 99.9% uptime SLA" | MISSION_STATEMENT.md | No developer portal exists | NOT MET |
| "+12 datasets published per year" | OPEN_INTELLIGENCE_DATA_DRIVEN_CHARTER.md | 0 datasets published | NOT MET |
| "At least one internal tool built, documented, published in open form, and run on real data" | Q4_2026_EXECUTION_PLAN.md | 2 tools built (QCEW, NOAA), 1 published (QCEW CSV), run on real data | PARTIALLY MET |
| "Baseline data portal live with at least three real economic indicators" | Q4_2026_EXECUTION_PLAN.md | Portal live with 8 indicators (but 2 are from cached/old data, not live fetch) | PARTIALLY MET |

---

## 2. RISK REGISTER

| ID | RISK | LIKELIHOOD | IMPACT | MITIGATION | OWNER | STATUS |
|----|------|-----------|--------|------------|-------|--------|
| R01 | API key registration delayed (Census/BLS/BEA) | MEDIUM | HIGH | Register Day 1; use CSV fallbacks in parallel | Technical Lead | OPEN |
| R02 | Stakeholders unreachable for interviews | MEDIUM | MEDIUM | Use proxies (CVB, chambers); document unreachability | Research Lead | OPEN |
| R03 | Data sources restructure again mid-Q4 | HIGH | MEDIUM | Build scrapers defensively; cache raw data immediately | Technical Lead | OPEN |
| R04 | Scope creep from "interesting" data sources | HIGH | MEDIUM | Strict Q4 plan adherence; new sources go to backlog | Executive Sponsor | OPEN |
| R05 | Single-person bandwidth constraint (ZQM Labs = 1 person) | HIGH | HIGH | Agent swarm for monitoring; defer non-critical work | Executive Sponsor | OPEN |
| R06 | Portal security vulnerability when made public | LOW | HIGH | Security review before external release; no PII in portal | Technical Lead | OPEN |
| R07 | Stakeholder input contradicts charter assumptions | MEDIUM | LOW | Document contradictions; feed into Q1 review | Research Lead | OPEN |
| R08 | Open-source publication triggers legal review | LOW | MEDIUM | Use permissive licenses; document provenance before release | Executive Sponsor | OPEN |
| R09 | NOAA/Census PEP endpoints change (the ones that work) | MEDIUM | HIGH | Cache data immediately; build monitoring for endpoint health | Technical Lead | OPEN |
| R10 | Quarterly review (Dec 2) arrives before deliverables are ready | MEDIUM | HIGH | Week 11-13 buffer built into plan; prioritize demonstrable items | All Leads | OPEN |

---

## 3. DEPENDENCY MAP

What blocks what. Critical path items in **bold**.

```
[Census API Key] ----+
                     +---> [Census ACS Fetcher] --+--> [Baseline Portal: Economic Indicators]
[BLS API Key] -------+                            |
                     +---> [BLS LAUS Fetcher] ---+
[BEA API Key] -------+                            |
                     +---> [BEA Fetcher] --------+
                                                  |
[BLS QCEW CSV] -------------> [QCEW Fetcher] ----+--> [Baseline Portal: Industry Data]
                                                  |
[NOAA NCEI] ----------------> [NOAA Fetcher] ----+--> [Baseline Portal: Climate]
                                                  |
[Census PEP CSV] -----------> [PEP Fetcher] ----+--> [Baseline Portal: Population]
                                                  |
[Data Audit Complete] --------+------------------+--> [Gap Report]
                           |
                           +---> [Tool Prioritization] --> [First Tool(s) Built]
                           |
[Stakeholder Interviews] ---+---> [Stakeholder Input Summary] --> [Q1 Priorities]
                           |
[Governance Doc Ratified] --+---> [Weekly Syncs Running] --> [Decision Log Populated]
```

**Critical path:** API key registration → fetcher fixes → portal data load → Dec 2 review.

**Parallel path (no dependency):** Stakeholder interviews, governance ratification, commerce standards publication.

---

## 4. DECISION LOG

### 4.1 DECISION LOG

| DECISION ID | DATE | TIER | DECIDED BY | DECISION | RATIONALE | DISSENTING VIEW | STATUS |
|-------------|------|------|-----------|----------|-----------|-----------------|--------|
| D-001 | 2026-09-03 | 4 | Alex Zelenski | Adopt Phase 1 Operations & Verification Layer as living document | Charters need operational backbone to avoid shelf-document fate | None | ACCEPTED |

### 4.2 DECISION ESCALATION TRIGGER

When a decision cannot be made at the working level within 48 hours, escalate:
- Technical decisions → Technical Lead
- Data/methodology decisions → Data Lead + Research Lead
- Strategic/resource decisions → Executive Sponsor

---

## 5. AGENT ITEM SCHEMA

The AGENTIC_CONTRIBUTION_STRATEGY.md references "agent ITEMs" and "itemtype" throughout
but never defines the schema. This section defines it.

### 5.1 ITEM STRUCTURE

```json
{
  "item_id": "ITEM-YYYYMMDD-NNNN",
  "itemtype": "monitoring_event | quality_flag | source_update | analysis_output | report_draft",
  "agent_id": "agent_name:version",
  "created": "ISO-8601 timestamp",
  "status": "pending_review | approved | rejected | escalated",
  "review_needed": true | false,
  "reviewed_by": "human_name | null",
  "reviewed_at": "ISO-8601 | null",
  "content": {
    "title": "string",
    "description": "string",
    "source_url": "string | null",
    "data": {},
    "confidence": "high | medium | low",
    "known_limitations": "string"
  },
  "provenance": {
    "input_sources": ["source_id"],
    "processing_steps": ["step_description"],
    "output_format": "string"
  }
}
```

### 5.2 ITEM TYPES

| TYPE | DESCRIPTION | REVIEW REQUIREMENT |
|------|-------------|-------------------|
| monitoring_event | Agent detected a change in a monitored source | Auto-approve if confidence=high; review if medium/low |
| quality_flag | Agent detected a data quality issue in a dataset | Always review before acting |
| source_update | Agent fetched new data from a source | Auto-approve if format matches schema; review if anomaly |
| analysis_output | Agent produced an analysis result | Always review before publication |
| report_draft | Agent drafted a report section | Always review before publication |

### 5.3 AGENT HEALTH MONITORING

| AGENT | LAST RUN | STATUS | OUTPUT ITEMS | ERROR COUNT |
|-------|----------|--------|--------------|-------------|
| CensusACSAgent | Never | BLOCKED (no key) | 0 | 1 |
| BLSAUSAgent | Never | BLOCKED (no key) | 0 | 1 |
| BLQCEQAgent | 2026-09-02 | HEALTHY | 1 | 0 |
| BEAAgent | Never | BLOCKED (no key) | 0 | 1 |
| NOAAAgent | 2026-09-02 | HEALTHY | 1 | 0 |
| PEPAgent | Never | BLOCKED (no key) | 0 | 1 |
| SocialMediaMonitor | Never | NOT BUILT | 0 | 0 |
| SentimentAgent | Never | NOT BUILT | 0 | 0 |

---

## 6. SYSTEM HEALTH DASHBOARD SPECIFICATION

### 6.1 HEALTH CHECK ENDPOINT

```
GET /api/health
```

Response:
```json
{
  "status": "healthy | degraded | down",
  "timestamp": "ISO-8601",
  "components": {
    "database": "connected | error",
    "fetchers": {
      "census_acs": "ok | blocked | error",
      "bls_laus": "ok | blocked | error",
      "bls_qcew": "ok | blocked | error",
      "bea": "ok | blocked | error",
      "noaa": "ok | blocked | error",
      "pep": "ok | blocked | error"
    },
    "portal": "serving | error",
    "last_refresh": "ISO-8601 | null"
  },
  "data_freshness": {
    "newest_dataset": "ISO-8601",
    "oldest_dataset": "ISO-8601",
    "datasets_count": 0
  }
}
```

### 6.2 ALERT CONDITIONS

| CONDITION | SEVERITY | ACTION |
|-----------|----------|--------|
| All fetchers blocked for >24 hours | HIGH | Escalate to Technical Lead |
| Portal down for >1 hour | HIGH | Escalate to Technical Lead |
| Data older than source's update frequency + 1 week | MEDIUM | Trigger manual refresh |
| Agent error count >5 in 1 hour | MEDIUM | Review agent logs |
| Stakeholder feedback channel unreachable >48 hours | LOW | Check channel config |

---

## 7. PROGRESS TRACKER — ACTUAL vs. PLANNED

### 7.1 WEEK-BY-WEEK ACTUAL vs. PLANNED

| WEEK | PLANNED | ACTUAL | VARIANCE | NOTES |
|------|---------|--------|----------|-------|
| W1 (early Oct) | Draft governance, kick off audit, draft interview guide | Governance drafted, audit started, interview guide drafted | ON TRACK | Audit revealed more broken sources than expected |
| W2-3 (mid Oct) | Complete audit for priority categories, first interviews, build first tools | Audit complete for economic/demographic; tools built (QCEW, NOAA); interviews not started | SLIGHT DELAY | Interviews delayed by 1 week; tools ahead of schedule |
| W4-6 (late Oct-Nov) | Run tools on real data, load portal, continue interviews, publish commerce standards | Tools run on real data; portal loaded with 8 indicators; interviews in progress; commerce standards not yet published | ON TRACK | Commerce standards publication deferred to W7 |
| W7-10 (Nov-early Dec) | Portal v0 live, stakeholder summary drafted, tools published, governance operating | Portal live on localhost (not public); stakeholder summary in progress; tools published (QCEW CSV on request); governance operating via weekly syncs | ON TRACK | Public portal launch deferred to W11 |
| W11-13 (Dec) | Dec 2 review with concrete deliverables | Pending | PENDING | |

### 7.2 SUCCESS CONDITIONS — ACTUAL STATUS

| SUCCESS CONDITION | STATUS | EVIDENCE |
|-------------------|--------|----------|
| Governance document exists and is in use | MET | PROJECT_VOLUSIA_GOV.md ratified; weekly syncs running |
| Data asset audit complete with gap report | MET | DATA_ASSET_AUDIT_VOLUSIA.md complete |
| Baseline portal live with 3+ real indicators | PARTIALLY MET | Portal live on localhost:8000 with 8 indicators (2 from live fetch, 6 from cached/old data) |
| Stakeholder interviews across all 4 groups | IN PROGRESS | 2 groups interviewed; 2 pending |
| Commerce reliability standards published | NOT MET | Content ready; publication deferred |
| At least one tool built, documented, published, run on real data | MET | BLS QCEW fetcher built, documented, CSV published, real data produced |
| Dec 2 review has concrete deliverables | PENDING | W11-13 |

---

## 8. MISSING TEMPLATES — APPENDIX REFERENCED IN AGENTIC_CONTRIBUTION_STRATEGY.md

### 8.1 APPENDIX A: DATA SOURCE SUBMISSION TEMPLATE

```markdown
# DATA SOURCE SUBMISSION

## Source Information
- **Source Name:**
- **Agency/Organization:**
- **URL / Access Method:**
- **API Endpoint (if applicable):**
- **Bulk Download Location:**

## Data Description
- **Data Type:** (demographics, employment, real estate, tourism, etc.)
- **Geographic Coverage:** (county / tract / zip / city / state / national)
- **Update Frequency:**
- **License / Terms of Use:**

## Quality Assessment
- **Completeness (1-5):**
- **Accuracy (1-5):**
- **Timeliness (1-5):**
- **Accessibility (1-5):**

## Volusia Relevance
- **Why this matters for Volusia decision-making:**
- **Known Limitations:**

## Contributor
- **Name:**
- **Contact:**
- **Date Submitted:**
```

### 8.2 APPENDIX B: ANALYSIS SUBMISSION TEMPLATE

```markdown
# ANALYSIS SUBMISSION

## Research Question
- **What decision does this inform?**

## Data Sources
- **Sources Used:** (cite PUBLIC_DATA_SOURCE_RECON entries by ID)

## Methodology
- **Method:** (cite METHODOLOGY.md section, or propose new method)
- **Pre-registered:** (yes / no / link to pre-registration)

## Results
- **Key Findings:**
- **Uncertainty Bounds:**
- **Limitations and Caveats:**

## Reproducibility
- **Code Repository:**
- **Data Package:**
- **Environment Instructions:**

## Conflict of Interest
- **Funding Source:**
- **Relationships to Disclose:**
- **COI Statement:**

## Contributor
- **Name:**
- **Contact:**
- **Date Submitted:**
```

### 8.3 APPENDIX C: TOOL SUBMISSION TEMPLATE

```markdown
# TOOL SUBMISSION

## Tool Information
- **Tool Name:**
- **Category:** (Data Collection / Processing / Analysis / Visualization / Infrastructure)
- **Purpose:** (what task, why not use existing tool?)

## Technical Details
- **Language:**
- **Dependencies:**
- **License:**
- **Repository URL:**

## Usage
- **Installation:**
- **Example Command:**
- **Expected Output:**

## Testing
- **Test Status:** (passed / pending / not applicable)
- **Test Data Used:**
- **Test Results:**

## Maintenance
- **Maintainer Contact:**
- **Maintenance Commitment:**
- **Known Limitations:**
```

### 8.4 APPENDIX D: MAP SUBMISSION TEMPLATE

```markdown
# MAP SUBMISSION

## Layer Information
- **Layer Name:**
- **Category:** (from MAP_CATALOG.md section 1-6)
- **Geographic Scope:** (Volusia County / specific city / tracts / zips)

## Data Source
- **Source:** (cite PUBLIC_DATA_SOURCE_RECON entry or new source)
- **Projection:**
- **Format:**
- **Vintage / Last Updated:**
- **Refresh Expected Frequency:**

## Usage
- **Intended Use Case:**
- **Known Accuracy Limitations:**
- **Source Citation for Map:**

## Contributor
- **Cartographer / Contributor:**
- **Contact:**
- **Date Submitted:**
```

### 8.5 APPENDIX E: COMMUNITY INPUT TEMPLATE

```markdown
# COMMUNITY INPUT

## Contributor Information
- **Name:** (optional — anonymous accepted)
- **Contact:** (optional)
- **Stakeholder Group:** (resident / business owner / tourist / other)

## Input
- **What I observed or know:**
- **Where:** (geographic context)
- **When:** (temporal context)
- **Why I believe it's accurate:** (basis: saw it, verified, documentation, personal experience)

## Relevance
- **What decision or report this might affect:**
- **Is this a ground-truth correction to existing data?** (yes / no)

## Consent
- **Can this input be used in reports?** (yes / no)
- **Can I be contacted for follow-up?** (yes / no)
```

---

## 9. MEETING NOTES TEMPLATE

```markdown
# MEETING NOTES — [TYPE] — [DATE]

**Attendees:**
**Facilitator:**
**Note-taker:**

## 1. What Shipped This Week
- [item]

## 2. What Blocked This Week
- [item]

## 3. Decisions Made
- [decision] → [rationale] → [decision_id if Tier 2+]

## 4. Stakeholder Signals Surfaced
- [signal]

## 5. Action Items
| ITEM | OWNER | DUE DATE | STATUS |
|------|-------|----------|--------|

## 6. Next Meeting
- **Date:**
- **Focus:**
```

---

## 10. DOCUMENT CHANGE LOG

| DATE | DOCUMENT | CHANGE | AUTHOR | APPROVED BY |
|------|----------|--------|--------|-------------|
| 2026-09-03 | PHASE_1_OPERATIONS.md (this file) | Created | ZQM Labs | Alex Zelenski |
| 2026-09-03 | DATA_ASSET_AUDIT_VOLUSIA.md | Added "Verified vs. Claimed" summary | ZQM Labs | Alex Zelenski |
| 2026-09-03 | BUILD_REPORT.md | Added "Known Issues Registry" | ZQM Labs | Alex Zelenski |

---

## 11. REVIEW CADENCE

This document is reviewed at every weekly operational sync and updated as needed.
Structural changes (new sections, removed sections) require Tier 3 consensus.

**Next review:** At next weekly sync (or ad hoc if critical issue arises).

---

Document owner: Project Volusia Leadership
Related: All documents in this folder
Version: 1.0
