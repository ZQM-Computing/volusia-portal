# PROJECT VOLUSIA — GOVERNANCE CHARTER
# Phase 1 Foundation Deliverable
# Date: 2026-09-03 | Version: 1.0
# Classification: Internal — Living Document

---

## 1. PURPOSE

This document defines who decides what, at what level, how often Project Volusia
reviews its own progress, and how disagreements are resolved. It exists so that
any new team member or partner can read it and immediately understand their role,
the decision boundaries, and the rhythm of the work.

Without governance, even the best charters become shelf documents. This is the
operational contract that makes the charters executable.

---

## 2. TEAM STRUCTURE AND ROLES

### 2.1 EXECUTIVE SPONSOR — Alex Zelenski
  SCOPE: Strategic direction, resource allocation, external representation,
         final decision authority on trade-offs that cross team boundaries.
  DECISIONS:
    - Strategic commits (which phase we are in, what ships when)
    - Resource allocation (what gets engineering time)
    - Public communications that speak for Project Volusia
    - Resolution of escalated disagreements between leads
  NOT responsible for:
    - Day-to-day technical decisions (Technical Lead owns those)
    - Data methodology details (Data Lead + Research Lead own those)

### 2.2 TECHNICAL LEAD (open)
  SCOPE: Architecture, tooling, deployment, code quality, technical debt.
  DECISIONS:
    - Technology selection (Python vs other, FastAPI vs Flask, SQLite vs Postgres)
    - Tool development priorities (which fetcher or dashboard gets built next)
    - Deployment approach (local, VPS, cloud)
    - Code review standards, CI structure, open-source release readiness
  ESCALATION TRIGGER:
    - Architecture changes that affect external stakeholders
    - Decisions requiring budget or infrastructure commitments beyond current means

### 2.3 DATA LEAD (open)
  SCOPE: Data sources, data quality, source reliability, indicator definitions.
  DECISIONS:
    - Which sources meet the tier standard for inclusion (COMMERCE_RESEARCH_RELIABILITY.md tier system)
    - Data cleaning methodology (how missing values are handled, how outliers are flagged)
    - Indicator definitions (what exactly "unemployment rate" or "median income" means for Volusia)
    - Data retention and refresh cadence
  ESCALATION TRIGGER:
    - Source inclusion that contradicts the tier standard
    - Methodology choices with material business implications

### 2.4 RESEARCH LEAD (open)
  SCOPE: Research methodology, stakeholder interview protocols, report standards.
  DECISIONS:
    - Interview guide design (what questions get asked)
    - Analysis approach (which statistical methods, how segments are defined)
    - Report structure (what goes in quarterly briefings, how findings are framed)
    - How stakeholder input gets weighted and prioritized
  ESCALATION TRIGGER:
    - Findings that challenge the assumptions in the existing charter documents
    - Stakeholder input that requires strategic reorientation

### 2.5 OPS / COMMUNICATIONS LEAD (open)
  SCOPE: Stakeholder-facing comms, meeting cadence, documentation, public portal content.
  DECISIONS:
    - How findings are communicated to the four stakeholder groups
    - Meeting facilitation and note-taking standards
    - Portal content updates, plain-language summaries
    - Feedback channel management (what gets logged, what gets escalated)
  ESCALATION TRIGGER:
    - Messaging that commits Project Volusia to a position or timeline
    - Public communications that could be perceived as speaking for Volusia County government

---

## 3. DECISION-MAKING FRAMEWORK

### 3.1 DECISION TIERS

  TIER 1 — AUTONOMOUS (no approval needed)
    - Day-to-day implementation details within a lead's scope
    - Tool-level code decisions (function names, library versions, log formats)
    - Interview scheduling and minor guide refinements
    - Documentation updates that don't change substance

  TIER 2 — INFORMED (lead decides, others informed at next sync)
    - New source inclusion that meets existing tier standard
    - Tool development priorities within the existing roadmap
    - Data cleaning choices within documented methodology
    - Content updates to the public portal

  TIER 3 — CONSENSUS (discussed with relevant leads before proceeding)
    - New tool categories not in TOOLS_CATALOG.md
    - Methodology changes that affect indicator definitions
    - Data source downgrades (moving a source from tier 1 to tier 2)
    - Stakeholder-facing commitments (we will publish X by Y date)

  TIER 4 — EXECUTIVE (Executive Sponsor decides)
    - Strategic direction changes
    - Phase transitions (Phase 1 → Phase 2)
    - Trade-offs that pit one charter objective against another
    - External partnerships or public statements on behalf of Project Volusia
    - Any decision that changes the scope defined in MISSION_STATEMENT.md

### 3.2 HOW DISAGREEMENTS GET RESOLVED

  1. Disagreeing parties state their positions in writing (one paragraph each)
  2. Relevant leads discuss at the next sync (or ad hoc if urgent)
  3. If consensus is not reached, the decision escalates one level up
  4. Executive Sponsor has final say on Tier 4 disputes; relevant lead has final
     say on Tier 2-3 disputes within their scope after hearing other perspectives
  5. Once a decision is made, the team commits to it — even the people who disagreed.
     Reopening requires new information, not just persistence.

---

## 4. MEETING CADENCE

### 4.1 WEEKLY OPERATIONAL SYNC
  WHEN: Weekly, same day/time (TBD by team)
  DURATION: 30 minutes
  FACILITATOR: Ops Lead (or Technical Lead if Ops not filled)
  ATTENDEES: All leads
  AGENDA:
    1. What shipped this week (5 min)
    2. What blocked this week (5 min)
    3. Decisions needed — Tier 2-3 items (15 min)
    4. Stakeholder signals surfaced (5 min)
  OUTPUT: Brief notes in a running sync log (file in this folder)

### 4.2 MONTHLY STAKEHOLDER-FACING REVIEW
  WHEN: First week of each month
  DURATION: 60 minutes
  FACILITATOR: Ops Lead
  ATTENDEES: All leads + invited stakeholders (rotating from the four groups)
  AGENDA:
    1. Key indicators update (what changed, what it means)
    2. Tools and portal progress
    3. Stakeholder feedback summary since last review
    4. Priorities for the coming month
  OUTPUT: Monthly review summary in this folder

### 4.3 QUARTERLY FORMAL REVIEW
  WHEN: Aligned with charter review cadence — first Monday of each quarter
         (Dec 2, Mar 2, Jun 2, Sep 2)
  DURATION: 90 minutes
  FACILITATOR: Executive Sponsor
  ATTENDEES: All leads + key partners
  AGENDA:
    1. Success conditions from previous review — met / not met
    2. Charter document review — any sections need updating
    3. Phase progress — on track / at risk / off track
    4. Resource assessment — capacity, gaps, needs
    5. Next quarter priorities and success conditions
  OUTPUT: Quarterly review summary, updated success conditions

### 4.4 ANNUAL MISSION REVIEW
  WHEN: December of each year (aligns with Dec 2 review)
  FOCUS: Does MISSION_STATEMENT.md still reflect reality? Are the guiding
         principles still the right ones? Is the roadmap still the right path?
  OUTPUT: Updated charter documents if needed

---

## 5. ESCALATION PATH

  WORKING LEVEL ISSUE
    → Discuss between relevant leads
    → Resolve at weekly sync
    ↓ (if unresolved after 1 week)
  ESCALATE TO TECHNICAL LEAD (for tooling/architecture issues)
    or DATA LEAD (for source/methodology issues)
    or EXECUTIVE SPONSOR (for strategic/resource issues)
    → Decision within 48 hours
    ↓ (if still blocked)
  EXECUTIVE SPONSOR DECISION — final

---

## 6. COMMUNICATION CHANNELS

  INTERNAL TEAM: Running notes file in Project-Volusia folder + weekly sync
  STAKEHOLDER INPUT: Logged in feedback channel (TBD — shared mailbox or form)
  PUBLIC COMMS: Reviewed by Ops Lead before release; Tier 4 comms approved by Exec Sponsor
  URGENT MATTERS: Direct message to relevant lead, followed by async log entry

---

## 7. DOCUMENT GOVERNANCE

  All Project-Volusia documents in this folder follow these rules:
  - Documents are dated and versioned
  - Changes are tracked in the document (not in a separate changelog for most docs)
  - Review cadence is stated at the bottom of each document
  - Obvious mistakes get fixed immediately; structural changes go through Tier 3 consensus

---

## 8. RELATED DOCUMENTS

  - MISSION_STATEMENT.md (north star)
  - COMMERCE_RESEARCH_RELIABILITY.md (research standards)
  - GUIDING_PRINCIPLES_VOLUSIA_COUNTY.md (stakeholder commitments)
  - OPEN_INTELLIGENCE_DATA_DRIVEN_CHARTER.md (open-source intelligence charter)
  - TIMELINE_AND_ROADMAP.md (phase plan)
  - Q4_2026_EXECUTION_PLAN.md (Q4 delivery plan)
  - DATA_ASSET_AUDIT_VOLUSIA.md (data source audit)

---

Document owner: Alex Zelenski / Project Volusia Leadership
Review cadence: Quarterly (at formal review)
Next review: 2026-12-02
