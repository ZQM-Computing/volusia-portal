# AGENTIC CONTRIBUTION STRATEGY — PROJECT VOLUSIA
# ====================================================
# Version: 1.0
# Date: 2026-09-03
# Classification: Operational Charter (addendum to MISSION_STATEMENT.md
#                and OPEN_INTELLIGENCE_DATA_DRIVEN_CHARTER.md)
#
# This document defines HOW humans and AI agents contribute to the
# Project Volusia knowledge system — the governance, pathways,
# lifecycle, incentives, and guardrails that make the system durable.
#
# Context: Project Volusia is a ZQM Labs initiative (Q4 2026–2027).
# ZQM Labs is a one-person operation (Alex Zelenski, zqmco) armed with a
# swarm of AI agents and high-powered tools, software, and computing
# technologies. The goal is to make the products of those tools widely
# available to Volusia County — not as a black-box AI output, but as
# verifiable, version-controlled, human-reviewed intelligence that
# residents, businesses, tourists, government, and investors can use to
# make better decisions.
#
# This contribution strategy is designed for a small team with a large
# agent swarm: lean human oversight (CGB), many agent monitors and
# processors, and a low-friction citizenry interface that lets Volusia
# residents, students, businesses, and institutions contribute without
# needing to know the system's internal structure.
#
# Related: MISSION_STATEMENT.md, OPEN_INTELLIGENCE_DATA_DRIVEN_CHARTER.md,
#          METHODOLOGY.md, DATA_CATALOG.md, PUBLIC_DATA_SOURCE_RECON.md,
#          TOOLS_CATALOG.md, Q4_2026_EXECUTION_PLAN.md

---

## 0. THE DESIGN PROBLEM

Project Volusia is not a wiki. Not a blog. Not a chatbot. It is a
**durable, verified, version-controlled intelligence system** whose
outputs (daily API calls, quarterly reports, tourist dashboards,
business owner toolkits) reach real stakeholders making real decisions.

The core tension:

   HUMAN CONTRIBUTION
     + Judged by real-world domain expertise
     + Motivated by mission, recognition, career, money
     + Slow, bounded by human time
     - Prone to fatigue, inconsistency, burnout
     - Cannot scale to fill a 24-event/yr publication cadence

   AGENTIC CONTRIBUTION
     + 24/7 availability, consistent formatting, fast iteration
     + Can monitor 47 data sources continuously
     + Can cross-reference 61 cataloged tables against new releases
     - Cannot be trusted to verify claims without review
     - Has no intrinsic stake in Volusia's wellbeing
     - Easy to game, easy to over-produce

The system must be **human-centered, agent-amplified**. Humans own
verification, source selection, and strategic judgment. Agents own
monitoring (continuous, boring, scalable), formatting, initial
synthesis, and flag-raising. The interface between them is structured
contribution — not freeform prompts.

---

## 1. GOVERNANCE ARCHITECTURE

### 1.1 Contribution Governance Body (CGB)

A named, accountable body — not "Project Volusia Leadership" as a
floating signifier.

**Composition (minimum viable):**

   ROLE                          | WHAT THEY DECIDE                          | WHO
   ------------------------------|-------------------------------------------|----------------
   Data Steward                  | Accept/reject data sources, table schemas | Research Team lead
   Methodologist                 | Approve new analysis methods before use   | Methodology owner
   Tool Owner                    | Register/modify tools in TOOLS_CATALOG    | Technical Team lead
   Report Lead                   | Approve report templates and schedules    | Comms Team lead
   GIS Lead                      | Approve new map layers to MAP_CATALOG     | GIS Team lead
   Community Liaison             | Curate human contributor submissions      | Liaison (new role)
   Agent Operations Lead         | Manage AI agent workflows, monitor health | Technical Team lead

**Meeting cadence:**

   - Weekly: 30-minute triage (new submissions, flagged agent outputs,
             source quality changes)
   - Monthly: 60-minute review (governance decisions, contributor
              management, methodology updates, metric review)
   - Quarterly: Full CGB + leadership review (strategy alignment,
                budget, portfolio review)

**Decision authority:**

   - Individual CGB members can accept routine submissions within
     their domain (routine data source addition, tool registration,
     standard report template use)
   - Decisions with material impact (new methodology, new indicator
     added to master metrics, public-facing claim change) require
     majority vote
   - Disputes escalate to full CGB → then to Project Volusia
     Leadership (named individuals, not a drift term)

**Record-keeping:**

   Every CGB decision is logged in a CONTRIBUTION_LOG.md (or equivalent
   structured record): date, decision, rationale, dissenting view
   (if any), and the contributor who submitted the item.

---

### 1.2 Domain Ownership Model

Every object in the system has an owner. Ownership is not property — it
is accountability.

   OBJECT TYPE          | OWNER (example)           | WHAT THEY OWN
   ----------------------|---------------------------|---------------------------
   Data source          | Data Steward              | Source registration, quality
                         |                           | scoring, vintage tracking
   Data table           | Data Steward              | Schema, update schedule,
                         |                           | quality flags, access controls
   Map layer            | GIS Lead                  | Projection, source citation,
                         |                           | refresh schedule
   Analysis method      | Methodologist             | When certified for use,
                         |                           | its documented limits
   Report template      | Report Lead               | Contents, standards, cadence
   Tool                 | Tool Owner                | Repository, documentation,
                         |                           | testing status
   Indicator/KPI        | Data Steward + Method-   | Definition, source, collection
                         | ologist (joint)          | method, update frequency
   Quarterly Briefing   | Report Lead               | Contents, schedule, review

**Ownership transfer:** If an owner leaves, their domain objects are
reassigned by CGB vote within 14 days. No object should be orphaned
for more than 30 days.

**Multiple owners:** Some objects have joint ownership (indicator =
Data Steward + Methodologist). When owners disagree, the CGB resolves.

---

## 2. CONTRIBUTION MODELS — HUMANS

### 2.1 Human Contributor Pathways

Six pathways, each with its own interface, requirements, and reward
structure.

---

#### PATHWAY A: DATA SOURCE CONTRIBUTOR

**Who:** Researchers, analysts, librarians, journalists, civic
technologists, subject-matter experts who discover or maintain
public data sources relevant to Volusia County.

**What they contribute:**

   - A new data source entry to PUBLIC_DATA_SOURCE_RECON.md (or its
     successor registry)
   - OR a quality update to an existing source (new vintage, changed
     access method, reliability flag)
   - OR a new table definition to DATA_CATALOG.md (with source lineage)

**Interface:**

   ```
   SUBMIT_DATA_SOURCE.md  (template — see Appendix A)
   ```

   A structured form, not freeform prose. Required fields:
   - Source name and agency/organization
   - URL / access method / API endpoint / bulk download location
   - Data type (demographics, employment, real estate, tourism, etc.)
   - Geographic coverage (county / tract / zip / city / state / national)
   - Update frequency
   - License / terms of use
   - Known limitations
   - Why this matters for Volusia decision-making
   - Contributor contact (for follow-up)

**Validation requirements:**

   - Data Steward verifies source exists and is accessible
   - Methodologist signs off if the source will be used for a
     material indicator (Tier 1 or 2 evidence standard, per
     COMMERCE_RESEARCH_RELIABILITY.md section 3.3)
   - GIS Lead reviews if geographic at tract/zip level
   - Community Liaison logs the contributor relationship

**Quality scoring:** The contributor proposes an initial quality score
(1-5 on completeness, accuracy, timeliness, accessibility). The CGB
may adjust after verification.

---

#### PATHWAY B: ANALYSIS CONTRIBUTOR

**Who:** Analysts, data scientists, academics, consultants, students,
volunteers who want to produce analysis that feeds into Project Volusia
reports.

**What they contribute:**

   - A completed analysis using a documented methodology (see
     METHODOLOGY.md section 3)
   - Source-cited, reproducible (code + data + method document)
   - Submitted for CGB review before publication in any Project Volusia
     channel

**Interface:**

   ```
   ANALYSIS_SUBMISSION.md  (template — see Appendix B)
   ```

   Required:
   - Research question (what decision does this inform?)
   - Data sources used (cite PUBLIC_DATA_SOURCE_RECON entries by ID)
   - Methodology (cite METHODOLOGY.md section, or propose new method
     with full documentation for Methodologist review)
   - Results (with uncertainty bounds, not just point estimates)
   - Limitations and caveats (honestly stated)
   - Reproducibility package (code + data + environment instructions)
   - Conflict of interest disclosure

**Validation requirements:**

   - Methodologist reviews the methodology before the analysis is
     considered reliable
   - Data Steward verifies data sources are correctly cited and
     current
   - Community Liaison checks that the contributor understands and
     agrees to the standards (especially: no misleading claims,
     publish null results, disclose COI)
   - CGB majority vote if the analysis touches a current KPI or
     report indicator

**Publication pathway:**

   If the analysis is reliable AND useful, the Report Lead determines
   where it is published: quarterly briefing appendix, standalone
   research note, methodology case study, or held for future use.

---

#### PATHWAY C: TOOL CONTRIBUTOR

**Who:** Developers, engineers, technical volunteers who build or
maintain tools.

**What they contribute:**

   - A new tool entry to TOOLS_CATALOG.md
   - The tool code (version-controlled)
   - Documentation (purpose, usage, dependencies, tested status)
   - Tested on sample data before contribution

**Interface:**

   ```
   TOOL_SUBMISSION.md  (template — see Appendix C)
   ```

   Required:
   - Tool name and category (Data Collection / Processing / Analysis /
     Visualization / Infrastructure)
   - Purpose (what task, why not just use an existing tool?)
   - Language and dependencies
   - Usage example (copy-pasteable)
   - Test status (passed / pending / not applicable)
   - License
   - Access method (repo URL, install instructions)
   - Open-source priority self-assessment (does this tool meet the
     OSS-first standard? If not, why?)
   - Maintainer contact and maintenance commitment
   - Known limitations

**Validation requirements:**

   - Tool Owner verifies the tool works as described (run the example)
   - CGB reviews if the tool will be made available to external users
   - Security review if the tool accesses external APIs or handles
     credentials
   - Documentation review before external release

---

#### PATHWAY D: MAP LAYER CONTRIBUTOR

**Who:** GIS professionals, cartographers, spatial analysts,
residents with local knowledge.

**What they contribute:**

   - A new map layer to MAP_CATALOG.md
   - The geospatial data (GeoJSON, Shapefile, GeoTIFF, etc.)
   - Documentation (projection, source, vintage, refresh schedule,
     usage notes)
   - The map itself (for publication in a report or dashboard)

**Interface:**

   ```
   MAP_SUBMISSION.md  (template — see Appendix D)
   ```

   Required:
   - Layer name and category (from MAP_CATALOG.md section 1-6)
   - Geographic scope (Volusia County / specific city / tracts / zips)
   - Data source (cite PUBLIC_DATA_SOURCE_RECON entry or new source)
   - Projection and format
   - Vintage / last updated
   - Refresh expected frequency
   - Intended use case
   - Known accuracy limitations
   - Source citation for the map itself
   - Cartographer / contributor contact

**Validation requirements:**

   - GIS Lead reviews projection, format, and source citation
   - Data Steward verifies the underlying data source
   - If the layer is for public release, Community Liaison checks
     that privacy/sensitivity concerns are addressed

---

#### PATHWAY E: REPORT CONTRIBUTOR

**Who:** Writers, editors, communicators, subject-matter experts who
help produce the quarterly briefs, monthly updates, and special reports.

**What they contribute:**

   - Draft sections of a scheduled report
   - Data summaries with source citations
   - Narrative that meets the REPORT_TEMPLATES.md standards
   - Fact-checking of existing report content

**Interface:**

   Direct contribution to a report's working draft (via shared
   document or version-controlled markdown). The Report Lead manages
   the draft and assigns sections.

**Validation requirements:**

   - Every fact must trace to a cited data source (from
     PUBLIC_DATA_SOURCE_RECON) or a cited analysis (from
     ANALYSIS_SUBMISSION with CGB approval)
   - Every number must have its source in the report's appendix
   - Uncertainty is stated honestly (ranges, confidence levels, known
     caveats)
   - Report Lead reviews for clarity, consistency, and standards
     compliance (8th-grade reading level, accessible visuals, no
     misleading scales)

---

#### PATHWAY F: COMMUNITY KNOWLEDGE CONTRIBUTOR

**Who:** Residents, business owners, community organizations, local
historians, students, teachers, parents, anyone with ground-level
knowledge that doesn't fit a formal data source — including input from
everyday citizenry: what you saw, what you experienced, what you know
from living and working in Volusia County.

**What they contribute:**

   - Qualitative context that explains the "why" behind the numbers
   - Ground-truth corrections ("that restaurant closed in March, the
     data says it's still open")
   - Local knowledge not yet in any public dataset (community
     facilities, informal economic activity, neighborhood history)
   - Feedback on report accuracy ("this section about our area is
     wrong in this specific way")
   - Personal experience narratives that put numbers in human context
     ("what housing affordability actually looks like for a family on
     a fixed income in DeLand")

**Interface:**

   ```
   COMMUNITY_INPUT.md  (template — see Appendix E)
   ```

   OR a simpler submission form (web form, email, SMS, phone hotline,
   library drop-box, school project submission, community meeting
   comment card — depending on channel). Content is:
   - What the contributor observed or knows
   - Where and when (geographic + temporal context)
   - Why they believe it's accurate (their basis: saw it happen,
     verified with someone, has documentation, personal experience)
   - What decision or report this might affect

**Validation requirements:**

   - Community Liaison logs the submission and responds within 5
     business days (acknowledgment even if no action)
   - If the input could affect a report or indicator, the relevant
     CGB member reviews it
   - Verification: where possible, the input is cross-checked against
     existing data sources or other community inputs
   - If verification goes the other way (the data is wrong, not the
     community input), the data source is flagged to the Data Steward

**Special handling:**

   Community knowledge is treated as Tier 4 evidence (Anecdote,
   per COMMERCE_RESEARCH_RELIABILITY.md section 3.3 — "illustrative
   only"). It can:
   - Trigger investigation of a data quality issue
   - Provide context in a report ("local business owners report...")
   - Generate a hypothesis for structured research
   It cannot, on its own, change an indicator value or make a factual
   claim in a public report.

**Additional citizenry channels (same pathway, multiple interfaces):**

   The Community Knowledge pathway accepts input through multiple
   channels to meet citizens where they are. All channels feed into
   the same submission pipeline and are subject to the same validation
   requirements. Channels include:

   1. **Direct submission** — web form, email, or structured template
      for contributors who prefer to write.

   2. **SMS / text message** — short-form input for contributors who
      prefer mobile. A longer follow-up may be requested if the
      initial text is too brief to act on.

   3. **Phone hotline** — voicemail or live reception for contributors
      who prefer voice. A staff member or agent transcribes the
      message into COMMUNITY_INPUT.md format.

   4. **Library drop-box / community center box** — physical submission
      for contributors without reliable internet. Library staff or
      community center staff collect and digitize submissions weekly.

   5. **Community meeting comment cards** — collected at public meetings,
      town halls, and community events.

   6. **School project submissions** — students and teachers submit
      class projects, local history research, survey results, and
      field observations through a dedicated school channel (see
      Pathway H below).

   7. **Social media monitoring** — with approval and transparent
      methodology (see Pathway G below).

---

#### PATHWAY G: SOCIAL MEDIA & PUBLIC FOOTPRINT CONTRIBUTOR

**Who:** Anyone who monitors, curates, or contributes from social media
and public online spaces — including Project Volusia staff, community
liaisons, teachers supervising student projects, and (with clear
transparency) AI agents operating under documented methodology.

**What they contribute:**

   1. **Social media intelligence (agent-curated or human-submitted):**

      - Sentiment signals from public social media about Volusia County
        (tourism sentiment, business reputation, community concerns)
      - Emerging issues detected in public conversation ("people are
        talking about the water quality at [beach]" / "there's a rumor
        about [road closure] that may affect tourism")
      - Public review aggregation (TripAdvisor, Google Reviews, Yelp,
        Facebook reviews of attractions, restaurants, hotels, businesses)
      - Event-driven spikes ("wedding bookings spike after a celebrity
        wedding in Ormond Beach" / "hashtag usage around [event]")

      **Methodological transparency required:**
      - What platform(s) were monitored
      - What query or keyword was used
      - What time period was covered
      - What was excluded (e.g., private accounts, deleted posts, spam)
      - What the known limitations are (platform demographics are not
        representative of Volusia's population — Twitter users skew
        younger and more urban than Volusia; Facebook users skew older;
        review platforms skew toward people with strong opinions)
      - Confidence level of the signal (directional vs. statistical)

      Per METHODOLOGY.md section 3.6 (Machine Learning) and section 4.4
      (Observational Research), any social media analysis must state its
      basis, limitations, and what it cannot tell you. Social media
      signals are treated as Tier 4 evidence (Anecdote/illustrative)
      unless aggregated and methodology-documented to a higher standard.

   2. **Crowdsourced intelligence from public online communities:**

      - Reddit threads about Volusia County (r/Volusia, local subs)
      - Facebook community groups (Daytona Beach community, New Smyrna
        Beach residents, etc.) — aggregated themes, not individual posts
      - Nextdoor posts about neighborhood conditions, safety, events
      - TripAdvisor / Google / Yelp review themes aggregated by location
        and time
      - Citizen science and public reporting platforms (e.g., post-hurricane
        damage reports from public forums)

      These are submitted as community inputs (Pathway F) when they come
      from human monitors, or as agent ITEMs (structured monitoring events)
      when produced by a SocialMediaMonitoringAgent following the
      documented methodology.

   3. **Public data from online platforms:**

      - Tourism board social media engagement data (publicly visible
        metrics like follower counts, engagement rates)
      - Event listing data from public calendars (Eventbrite, local
        newspaper events, chamber of commerce calendars)
      - Business listing data (Google My Business public profiles, Yelp
        business listings, TripAdvisor listings — publicly available
        metadata, not private data)

      These contribute to the data catalog (DATA_CATALOG.md) and are
      treated as data sources (Pathway A) when they meet the
      documentation standards.

**Interface:**

   For social media monitoring results:
   ```
   SOCIAL_MEDIA_INPUT.md  (template — see Appendix E modified below)
   ```
   OR agent ITEM with itemtype "monitoring_event" or "quality_flag" when
   produced by a SocialMediaMonitoringAgent.

   For crowdsourced intelligence:
   ```
   COMMUNITY_INPUT.md  (template — see Appendix E)
   ```
   Same channel as Pathway F, with "source: social media / public forum"
   noted in the submission.

   For public platform data:
   ```
   DATA_SOURCE_SUBMISSION.md  (template — see Appendix A)
   ```
   When a public platform (TripAdvisor, Google My Business, etc.) is
   being registered as a data source.

**Validation requirements:**

   - Social media monitoring methodology must be documented before the
     results are used for anything beyond hypothesis generation
   - Platform demographics and known biases must be stated when reporting
     social media signals
   - Social media signals are never presented as representative of the
     full Volusia population without explicit caveat (platform users are
     a self-selected sample, not a probability sample)
   - Individual social media posts are not published in Project Volusia
     reports — only aggregated themes, with the aggregation method
     documented
   - Private social media content is never collected or used — only what
     is publicly visible on the platform at the time of monitoring
   - Post deletion risk must be acknowledged: content visible today may be
     deleted tomorrow, so social media intelligence has a short shelf life
     and should be captured and stored promptly
   - If a human monitors social media and submits findings, the same
     COMMUNITY_INPUT.md validation applies (logged within 5 business days,
     verified where possible, acknowledged even if no action)

**Special handling:**

   Social media intelligence is the most noise-prone input channel in the
   system. It is valuable for detecting emerging issues early, understanding
   public sentiment directionally, and capturing real-time tourist/business
   reactions. It is NOT reliable for:
   - Estimating population-level opinions or behaviors
   - Making factual claims about Volusia without independent verification
   - Replacing structured surveys or data sources for material decisions

   Social media signals can:
   - Trigger a deeper investigation ("people are saying the water is brown
     at [beach] — check water quality data and recent weather events")
   - Provide color and context in reports ("social media reactions to the
     summer music festival were mixed, with [theme] and [theme] emerging")
   - Feed the sentiment analyzer tool (TOOLS_CATALOG.md) if a structured
     sentiment pipeline is built

   AI agents that monitor social media (SocialMediaMonitoringAgent,
   ReviewAggregatorAgent, SentimentAgent) must operate under the same
   guardrails as other agents (section 3.1-3.2): structured ITEMs, no
   publication without human sign-off, labeled with agent ID and version,
   flag "review_needed" when they cannot verify.

---

#### PATHWAY H: EDUCATIONAL INSTITUTION CONTRIBUTOR

**Who:** K-12 teachers and students, college and university faculty,
researchers, students, interns, and staff from educational institutions
in and around Volusia County — including Volusia County Schools, Daytona
State College, Embry-Riddle Aeronautical University, Bethune-Cookman
University, Stetson University, Daytona State College, and other
regional institutions — as well as educational institutions outside
Volusia County that want to study or contribute to Volusia County
intelligence.

**What they contribute:**

   1. **Classroom and course projects:**

      - Student research projects on Volusia topics (demographics, local
        history, environment, economics, tourism, agriculture, etc.)
      - Class surveys and fieldwork results (with IRB or teacher approval
        where applicable)
      - Data analysis projects using Project Volusia data (with proper
        citation and methodology documentation)
      - Mapping and GIS projects (student cartography, spatial analysis)
      - Service-learning projects that collect community data (e.g., a
        class survey of local business digital adoption, a student audit
        of park conditions, a school habitat survey)

      These are submitted via:
      - Teacher or faculty sponsor submitting on behalf of the class/project
        (recommended for K-12 — the teacher vouches for the work)
      - Individual student submission with faculty sponsor approval (for
        higher education — the sponsor confirms the work meets academic
        standards)
      - Direct student submission for older students who want to contribute
        independently (subject to the same validation as any other Pathway F
        or B submission)

   2. **Faculty and student research:**

      - Academic research on Volusia topics (published or unpublished)
      - Pilot studies and preliminary findings
      - Literature reviews on Volusia-relevant topics
      - Methodological innovations tested on Volusia data
      - Thesis and dissertation work that includes Volusia data or analysis

      These follow the ANALYSIS_SUBMISSION.md pathway (Pathway B) when they
      are analysis, or the DATA_SOURCE_SUBMISSION.md pathway (Pathway A)
      when they produce new data sources, or the COMMUNITY_INPUT.md pathway
      (Pathway F) when they are qualitative observations or context.

      **Academic review standard:**
      Faculty-sponsored work from a recognized educational institution is
      treated as having passed an academic quality gate (the sponsor confirms
      the work meets the institution's standards for the level — high school
      project, undergraduate paper, master's thesis, dissertation). This does
      NOT replace CGB review for Project Volusia publication — it means the
      CGB accepts the methodology as academically sound and focuses its review
      on relevance to Volusia decision-making, source documentation, and
      clarity for the intended audience.

   3. **Citizen science and community-based monitoring:**

      - Student-led environmental monitoring (water quality, air quality,
        wildlife counts, beach condition surveys)
      - Community-based data collection (class surveys of local conditions,
        neighborhood assessments, oral history projects)
      - K-12 project-based learning that generates data about Volusia County

      These are treated as community inputs (Pathway F) with the additional
      context that they come from educational projects. The teacher or faculty
      sponsor confirms the project design and data collection method.

   4. **Educational use of the Project Volusia knowledge base:**

      Teachers and faculty can request access to Project Volusia data and
      tools for classroom use. This is not a "contribution" in the sense of
      adding to the knowledge base — it's a consumption pathway that may lead
      to future contributions when students produce work that is shared back.

      Educational use requests are handled by the Community Liaison. Schools
      and institutions that regularly use Project Volusia resources and
      contribute back become "Educational Institution Partners" (see incentives
      below).

**Interface:**

   For class projects and coursework:
   ```
   SCHOOL_PROJECT_SUBMISSION.md  (template — see Extended Appendix E below)
   ```
   OR COMMUNITY_INPUT.md when the project output is qualitative observation
   or context. OR ANALYSIS_SUBMISSION.md when the project is a data analysis
   that could feed a report.

   For faculty research:
   ```
   ANALYSIS_SUBMISSION.md  (template — see Appendix B)
   ```
   OR DATA_SOURCE_SUBMISSION.md when the research produces a new data source.
   The faculty sponsor's name and institution are included.

   For citizen science and community monitoring:
   ```
   COMMUNITY_INPUT.md  (template — see Appendix E)
   ```
   With "educational_institution" field noting the school or institution and
   the project type.

   For educational use requests:
   ```
   EDUCATIONAL_USE_REQUEST.md  (template)
   ```
   Fields: institution, teacher/faculty name, course or project, what
   Project Volusia resources are requested, what students will do with them,
   timeframe, any data the class will collect that could be shared back.

**Validation requirements:**

   - K-12 submissions: teacher or faculty sponsor confirms the work is
     genuine student work, explains the project design, and takes
     responsibility for the submission's accuracy to the best of their
     knowledge. The Community Liaison reviews with the understanding that
     student work may not meet professional analyst standards — the review
     is about whether the contribution is useful and honest, not whether it
     meets a professional analyst bar.

   - Higher education submissions: faculty sponsor confirms the work meets
     the institution's standards for the level (undergraduate, master's,
     doctoral). The CGB applies the standard analysis review (Pathway B)
     for work that would feed a report, but may treat faculty-sponsored
     work as having passed an initial academic quality check.

   - Student privacy: submissions from K-12 students must protect student
     privacy. Student names are not published without explicit opt-in
     permission from the student and (for minors) the parent or guardian.
     Student work is attributed to the school and (optionally) to the
     student by first name only, or to "students of [school]", or anonymously,
     depending on the student's/family's preference.

   - Academic integrity: submissions that appear to be plagiarized or
     generated by an AI without disclosure are not accepted. If a student
     used AI tools as part of their work, this must be disclosed in the
     submission (the teaching moment here is about transparency, not
     prohibition — see incentives below).

   - IRB and human subjects: if a school project involves surveying people
     beyond the class, the teacher or faculty sponsor is responsible for
     ensuring appropriate consent and privacy protections. Project Volusia
     does not conduct human subjects research without appropriate oversight.

   - Data quality: student-collected data (surveys, observations, measurements)
     is reviewed for obvious issues (incomplete data, inconsistent methods,
     small samples) by the Data Steward. Student data is not automatically
     added to the data catalog — it is added when the teacher/faculty sponsor
     and Data Steward agree the data is reliable enough for catalog inclusion.

**Special handling:**

   Educational institution contributions are a unique category because they
   combine public benefit (students learning to do real analysis on real local
   data) with a quality variation challenge (a senior thesis and a 5th-grade
   class survey are both valuable, but at very different evidentiary standards).

   The system handles this by:

   1. **Acknowledging the educational context** — every submission from an
      educational institution notes the institution, the course or project,
      and the level (K-12, undergraduate, graduate). This context is preserved
      in the contributor record and, where appropriate, in the published output
      ("This analysis was produced by students in [course] at [institution] as
      a class project. It has been reviewed by [faculty sponsor] and the Project
      Volusia Research Team for relevance and methodology.")

   2. **Treating educational contributions as Tier 4 (anecdotal/illustrative)
      by default, with a path to higher tiers:**

      A well-designed class project with proper methodology, a faculty sponsor,
      and reproducible data can be elevated to Tier 3 (expert interview /
      structured survey) or even Tier 2 (structured survey with good sample
      and calibrated questions) if the CGB Methodologist and Data Steward
      agree the methodology supports it. The elevation path is:
      - Student/faculty submits work
      - Community Liaison and relevant CGB members review with an eye toward
        both educational quality AND whether the work could be elevated
      - If the work is strong enough, the CGB can reclassify it for a
        specific use (e.g., "this survey is good enough to cite as directional
        evidence in the Resident Well-Being Report")
      - If not, it stays Tier 4 and is still used for context, hypothesis
        generation, and as a record of student engagement with Volusia data

   3. **Valuing the educational contribution even when it's not publication-ready:**

      A 5th-grade class that maps local trees, a high school statistics class
      that surveys local business digital adoption, and a college class that
      analyzes Volusia tourism data all contribute to the system's mission even
      if their work doesn't meet professional publication standards. The
      contribution is recognized, the students are credited (within privacy
      constraints), and the work is archived as a record of community engagement
      with Volusia intelligence.

   4. **Protecting students from being burdened by the system:**

      Project Volusia does not require student work to meet a standard that
      the students cannot reasonably meet for their level. A K-12 submission
      that arrives without a teacher sponsor is returned to the school, not
      rejected as invalid. A college submission that is incomplete is returned
      for revision with specific feedback, not silently rejected.

---

#### PATHWAY I: CITIZENRY DIRECT CONTRIBUTION

**Who:** Any resident of Volusia County, any person who lives, works, visits,
or invests in Volusia County, and any community organization, business, or
institution that wants to contribute directly to the Project Volusia knowledge
base without going through a specific channel above.

**What this pathway is for:**

Pathways A-H cover specific types of contributions (data sources, analysis,
tools, maps, reports, community knowledge, social media, educational work). This
pathway is the catch-all for citizenry direct contribution — things that don't
fit the above, or that a contributor is unsure how to categorize.

**What they contribute:**

   - Anything a citizen wants to contribute that is relevant to Volusia County
     intelligence and that the contributor has a basis for knowing or believing
   - Questions or suggestions about the Project Volusia system itself
   - Corrections to the system (e.g., "your data catalog lists a source that's
     no longer available")
   - Ideas for new indicators, reports, maps, or tools
   - Feedback on the contribution process itself

**Interface:**

   ```
   DIRECT_CONTRIBUTION.md  (template — see Appendix E variant)
   ```
   OR any of the existing templates if the contributor knows what type of
   contribution they're making. OR a general-purpose web form, email, SMS, or
   phone message that the Community Liaison routes to the appropriate pathway.

**Validation requirements:**

   Same as Pathway F for community knowledge. For contributions that clearly
   belong to another pathway (A-H), the Community Liaison routes them to the
   appropriate pathway and the contributor is notified. The contributor does
   not need to know the pathway structure — they just need to submit.

**Special handling:**

   This pathway exists so that the system does not become a maze of forms that
   prevents citizens from contributing. A citizen who knows what they want to
   contribute but doesn't know which pathway to use submits via this pathway,
   and the system figures out the rest. The Community Liaison owns this routing.

   The direct contribution form is the simplest possible interface: "What do you
   want to contribute? (free text) What's your basis for knowing this? (free text)
   What decision or report do you think this relates to? (free text, optional)
   Contact info (optional)."

---

### 2.2 Human Contributor Recognition and Incentives

**Tangible incentives:**

   - Credit in published reports (byline for major contributions,
     acknowledgment for smaller ones)
   - Contributor profile on the public portal (optional — opt-in only)
   - Quarterly contributor recognition (named, not anonymous)
   - Priority access to data and tools (for credible, consistent
     contributors)
   - Skill development: methodological training, data access support,
     mentorship from CGB members
   - Paid contributions where funding exists (grants, contracts,
     sponsor-funded analyst roles)

**Incentives for educational institution contributors (Pathway H):**

   - **For teachers and faculty:** recognition in Project Volusia publications
     (e.g., "Data for this section was contributed by students in [course] at
     [institution], under the supervision of [faculty name]"), access to Project
     Volusia data and tools for classroom use, support for curriculum alignment
     (help connecting Project Volusia data to course objectives), and (where
     funding exists) grants or stipends for classroom data projects.

   - **For students:** public credit for their work (within privacy constraints),
     a real-world portfolio piece that demonstrates ability to analyze local data,
     mentorship and feedback from Project Volusia analysts and CGB members,
     potential internship or research opportunities with Project Volusia or its
     partners, and (for higher education) a pathway to publish class work that
     meets the standard for inclusion in Project Volusia reports — a rare
     opportunity for undergraduate work to reach a public audience and influence
     real decisions.

   - **For schools and institutions:** recognition as an Educational Institution
     Partner (public acknowledgment, subject to institutional approval), a
     partnership relationship with Project Volusia that can support grant
     applications, service-learning course design support, and priority access to
     educational resources and data for classroom use.

   - **For the educational ecosystem:** Project Volusia becomes a resource that
     local schools and colleges can use to give students hands-on experience with
     real data about their own community. This is a long-term talent pipeline for
     the system (students who learn to contribute early may become adult
     contributors later) and a way to build community literacy about data and
     analysis.

**Incentives for social media contributors (Pathway G):**

   - Contributors who monitor social media and submit organized, useful signals
     (not just raw links or noise) are recognized as contributing a specialized
     skill (public conversation intelligence). This is valuable experience for
     anyone interested in media monitoring, community management, tourism
     marketing, or public relations — all relevant to Volusia's tourism and
     business ecosystem.
   - Where funding exists, structured social media monitoring (regular, documented,
     methodologically sound) can be a paid role (part-time community monitor,
     tourism sentiment analyst, etc.).
   - Social media contributors who consistently produce useful signals (not noise)
     gain access to more advanced monitoring tools and collaboration with the
     Project Volusia communications and tourism teams.

**Incentives for citizenry direct contributors (Pathway I):**

   - Simple recognition: a contributor who submits a useful correction, idea, or
     observation gets an acknowledgment (if they opt in) and the satisfaction of
     having their knowledge included in a system that reaches real stakeholders.
   - No expert credential is required. A resident who knows their neighborhood
     better than any dataset does is a valuable contributor, even if they've never
     written a report or analyzed data.
   - The system meets citizens where they are — email, SMS, phone, library drop-box,
     community meeting comment card, school project, social media. The act of
   contributing should be as easy as the contribution type allows.

**Non-tangible incentives:**

   - Mission alignment (the contributor's work reaches real
     stakeholders and influences real decisions)
   - Portfolio building (publicly citable work with documented
     methodology)
   - Community (being part of a shared effort, not a one-off)
   - Transparency (seeing how their contributions are used)

**Contribution quality tracking:**

   Every contributor has a CONTRIBUTION_RECORD.md (or structured
   record) tracking:
   - Submissions made
   - Acceptance rate (how many passed CGB review)
   - Time-to-review (how long their submissions waited)
   - Quality score (average quality score of accepted submissions)
   - Repeatability (do they contribute consistently or in bursts?)
   - Community feedback (were other contributors satisfied with their
     work?)

   For educational institution contributors, the record also tracks:
   - Institution and course/project
   - Student privacy preferences (names published? first-name-only? anonymous?)
   - Educational level (K-12, undergraduate, graduate)
   - Whether the work was elevated to a higher evidence tier

   The record informs recognition, access privileges, and where the
   contributor needs support (e.g., a contributor with low acceptance
   rate gets method review support, not rejection).

---

## 3. CONTRIBUTION MODELS — AI AGENTS

### 3.1 What AI Agents Are For

AI agents are **amplifiers, not authors**. They expand capacity in areas
where human time is the bottleneck and the work is structured. They
never make final claims about Volusia without human verification.

**Agent-appropriate tasks:**

   1. **Continuous monitoring** — Watch 47 data sources (per
      PUBLIC_DATA_SOURCE_RECON.md) for updates, new releases, broken
      links, changed formats. Flag when something changes.

   2. **Data acquisition automation** — Run the tools in
      TOOLS_CATALOG.md on schedule: pull Census data, scrape BLS,
      fetch NOAA weather. Log what was pulled, when, and the vintage.

   3. **Initial data processing** — Run cleaners, normalizers, joiners
      on new data. Produce a draft processed dataset, flagged for
      human review.

   4. **Draft synthesis** — Given approved data and a documented
      methodology, produce a draft analysis section with sources cited.
      Marked as "DRAFT — AI-generated, human-verified" until a human
      signs off.

   5. **Quality flagging** — Compare new data against historical
      baselines. Flag anomalies: sudden jumps, missing values, format
      changes, values outside expected ranges.

   6. **Format and consistency enforcement** — Ensure all contributions
      meet the standards in METHODOLOGY.md and REPORT_TEMPLATES.md:
      citation format, uncertainty language, chart conventions, visual
      accessibility.

   7. **Cross-referencing** — When a new data source is added, search
      across all 61 cataloged tables for related data. Surface relevant
      tables, highlight potential join keys, note differences in
      methodology or vintage.

   8. **Backlog management** — Track pending submissions (human and
      agent), route to the right CGB member, escalate stale items.

**Agent-inappropriate tasks (human-only):**

   - Source selection for a new indicator (requires judgment about
     authority, methodology, coverage — an agent can surface options,
     a human decides)
   - Methodology certification (a new method requires human review of
     assumptions, limitations, and fit-for-purpose)
   - Final claims in public-facing reports (a human signs off)
   - Strategic prioritization (an agent can flag opportunities, a
     human decides what to pursue)
   - Conflict-of-interest assessment
   - Crisis response and emergency reporting

---

### 3.2 Agent Architecture

#### 3.2.1 Agent Tiers

**TIER 1 — MONITORING AGENTS (always on, low autonomy)**

   What they do:
   - Poll data sources on a schedule (matching each source's update
     frequency from PUBLIC_DATA_SOURCE_RECON.md)
   - Detect changes (new vintage, new format, link rot, content
     changed)
   - Run data acquisition tools
   - Log results to a structured feed

   Autonomy: None. They observe and report. No decision-making.

   Example:
   ```
   CensusMonitoringAgent
   - Polls Census ACS API daily for new data releases matching
     registered tables
   - Logs: source, table, vintage, file size, checksum, timestamp
   - Flags: new vintage available, data size changed >10%,
     API response changed (new columns, different format)
   - Creates a SUBMISSION_ITEM.md for the Data Steward
   ```

   Human interaction: The agent creates a structured submission item.
   The Data Steward reviews and accepts/rejects within 3 business days.

---

**TIER 2 — PROCESSING AGENTS (scheduled, medium autonomy)**

   What they do:
   - Run processing tools (cleaner, normalizer, aggregator, geocoder)
     on new data
   - Produce draft processed datasets
   - Flag quality issues (missing values, outliers, format issues)

   Autonomy: Can run a predefined processing pipeline on new data.
     Cannot change the pipeline without human approval.

   Example:
   ```
   DataProcessingAgent
   - Detects new ACS vintage from monitoring feed
   - Runs census_api_wrapper → data_cleaner → aggregate_to_county
     (the pipeline defined in TOOLS_CATALOG.md)
   - Produces: raw/ACS_2023_county.csv, processed/ACS_2023_county_clean.csv,
     aggregated/ACS_2023_volusia_summary.csv
   - Logs: pipeline version, input vintage, output file, row counts,
     flagged issues (columns with >5% missing, values outside
     historical range)
   - Creates a SUBMISSION_ITEM.md for the Data Steward:
     "New processed dataset ready — review and publish?"
   ```

   Human interaction: Data Steward reviews the processed output,
   addresses flagged issues, and publishes if acceptable.

---

**TIER 3 — SYNTHESIS AGENTS (on-demand, high autonomy within bounds)**

   What they do:
   - Given a defined task (e.g., "draft the employment section of the
     Q3 2026 Quarterly Economic Briefing, using the methodology in
     METHODOLOGY.md section 3.1 and 3.2, citing sources from
     PUBLIC_DATA_SOURCE_RECON.md"), produce a draft section
   - Use only data that has been verified and published by a human
   - Cite sources with the standard format
   - State uncertainty honestly per METHODOLOGY.md section 5.3
   - Flag anything that would require a new analysis or a Tier 1/2
     evidence decision

   Autonomy: Can draft, can search, can format. Cannot make claims
     not supported by the provided data. Cannot decide to use a new
     data source without Data Steward approval. Cannot publish.

   Example:
   ```
   BriefingSynthesisAgent
   - Receives task: "Draft Q3 2026 employment section"
   - Retrieves: BLS LAUS data (published, current vintage), QCEW data
   - Produces draft with:
     * Employment trend narrative (using descriptive methodology,
       section 3.1 of METHODOLOGY.md)
     * Source citations in standard format
     * Uncertainty language ("data is 1-month lagged", "seasonal
       adjustment applied")
     * Flag: "QCEW data is 6-month lagged — current picture incomplete.
       Recommend briefing note on this limitation."
   - Output marked: "DRAFT — AI-generated, requires human verification
     before publication"
   - Sent to Report Lead for review and human sign-off
   ```

   Human interaction: Report Lead reviews the draft, verifies claims
     against source data, edits for clarity and accuracy, and signs
     off (or returns for revision).

---

#### 3.2.2 Agent Communication Protocol

All agent actions produce structured outputs, never freeform text in
the knowledge base. The protocol:

```
ITEM = {
  itemtype:             "monitoring_event" | "processing_result" |
                        "synthesis_draft" | "quality_flag" |
                        "cross_reference" | "submission_item",
  agent_id:             "census_monitor_v1" | "acs_processor_v1" |
                        "briefing_synth_v1" | ...,
  timestamp:            ISO 8601,
  source:               which data source / tool / method this relates to,
  confidence:           0.0-1.0 (agent's self-assessed confidence,
                        NOT a claim of correctness),
  content:              structured payload (the actual output),
  flags:                ["new_vintage", "format_changed", "missing_values",
                        "out_of_range", "review_needed", ...],
  next_action:          "human_review_required" | "auto_accept" |
                        "agent_followup",
  human_owner:          which CGB member owns this item (for routing)
}
```

This is machine-parseable and human-readable. It lets agents queue
work for humans without flooding them with unstructured output.

---

#### 3.2.3 Agent Health and Behavior Monitoring

**Each agent has a health record:**

   - Last successful run
   - Run frequency (target vs actual)
   - Error rate (failed runs / total runs)
   - Drift detection: is the agent producing the same type of output
     it was designed for, or has it drifted?
   - Cost monitoring: API calls, compute, storage
   - Output quality: spot-check agent outputs against human-verified
     baselines periodically

**Agent behavior rules:**

   1. An agent that cannot verify its output against a source must
      flag "review_needed" and not present the output as reliable.
   2. An agent that encounters an unfamiliar situation must stop and
      escalate to a human rather than improvise.
   3. An agent that produces output significantly different from its
      historical pattern must flag the change — it may be correct
      (real change in Volusia) or a bug (agent drift).
   4. An agent must never publish to a public channel without human
      sign-off. Ever.
   5. An agent's output is labeled with the agent's ID, version, and
      a timestamp — so any output can be traced back to the agent
      that produced it.

**Agent retirement:**

   When an agent is decommissioned (replaced, source no longer
   available, no longer needed), its health record is archived but
   its outputs remain in the knowledge base with their original
   attribution. The system doesn't retroactively re-validate old
   agent output — but if a claim is questioned, the original agent's
   version and the data it used are retrievable.

---

## 4. CONTRIBUTION LIFECYCLE

### 4.1 The Submission-to-Publication Pipeline

Every contribution — human or agent — flows through the same lifecycle:

```
STEP 1: SUBMISSION
        ||
        ||  Item arrives (human form, agent ITEM, email, SMS)
        ||
STEP 2: LOGGING
        ||
        ||  Community Liaison (or automated router for agent items)
        ||  assigns: item_id, timestamp, submitter, category,
        ||  intended destination (which report/indicator/table/map)
        ||
STEP 3: ROUTING
        ||
        ||  Routed to the authoritative CGB member(s) for the domain
        ||  (Data Steward for data sources, Methodologist for methods,
        ||   Tool Owner for tools, GIS Lead for maps, etc.)
        ||
STEP 4: REVIEW
        ||
        ||  Reviewer checks:
        ||  - Does it meet the standards for its type?
        ||  - Are sources correctly cited?
        ||  - Is methodology appropriate?
        ||  - Is the contribution true to what it claims?
        ||  - Any conflicts of interest to disclose?
        ||
STEP 5: DECISION
        ||
        ||  ACCEPT: Item enters the knowledge base
        ||    - If it affects a public report/indicator: flagged
        ||      for the responsible report lead
        ||    - If it's a new data source: added to PUBLIC_DATA_SOURCE_RECON
        ||    - If it's a tool: added to TOOLS_CATALOG with tool owner
        ||
        ||  REQUEST_REVISION: Returned to submitter with specific
        ||    feedback. Resubmit after revision.
        ||
        ||  REJECT: Documented rationale. Submitted item archived
        ||    (rejected items are visible in the log — no file-drawering
        ||    of contributions, even rejected ones)
        ||
STEP 6: INTEGRATION
        ||
        ||  Item is placed in the correct location:
        ||  - Data → raw/ or processed/ directory, catalog updated
        ||  - Analysis → research notes directory, linked to report
        ||  - Tool → tools/ directory, catalog updated
        ||  - Map → maps/ directory, catalog updated
        ||  - Report section → working draft
        ||
STEP 7: VERIFICATION (where applicable)
        ||
        ||  For items that affect public outputs:
        ||  - Data Steward spot-checks the data
        ||  - Methodologist confirms methodology if new
        ||  - Community Liaison verifies community input against
        ||    available sources (when possible)
        ||
STEP 8: PUBLICATION (if the item is destined for a public output)
        ||
        ||  Report Lead or responsible owner incorporates into:
        ||  - Quarterly briefing, monthly update, annual report,
        ||    business owner toolkit, tourist report, etc.
        ||  Published with source citations, methodology notes,
        ||  and uncertainty language per REPORT_TEMPLATES.md standards
        ||
STEP 9: POST-PUBLICATION REVIEW
        ||
        ||  After publication:
        ||  - Did the data hold up? (Were there corrections later?)
        ||  - Did the prediction come true? (For forecasts)
        ||  - Did anyone flag an error?
        ||  - Was the contribution useful? (Feedback from stakeholders)
        ||
        ||  Lessons feed back into the system:
        ||  - Data source quality scores updated
        ||  - Methodology refined if needed
        ||  - Contributor recognition updated
```

---

### 4.2 Special Lifecycles

#### 4.2.1 Agent-Generated Submissions

Agent items skip manual submission (they generate structured ITEMs
automatically). But they still flow through routing → review →
decision → integration → verification → publication.

The difference: the "reviewer" is the CGB member who owns the domain,
not the Community Liaison. And the agent's ITEM includes a confidence
value and flags so the reviewer can triage efficiently.

Example:

   ```
   09:00 — CensusMonitoringAgent detects new ACS vintage
   09:01 — ITEM created: {"itemtype": "monitoring_event",
        "flags": ["new_vintage"], "human_owner": "Data Steward",
        "next_action": "human_review_required"}
   09:05 — Routed to Data Steward's queue
   ]
   ]
   Day 2 — Data Steward reviews
         - Confirms the new vintage is real and accessible
         - Creates a new data source entry in PUBLIC_DATA_SOURCE_RECON
         - Assigns quality score (preliminary: 4/5, pending full assessment)
         - Creates processing item for DataProcessingAgent
   Day 3 — DataProcessingAgent runs, produces cleaned dataset
         - Data Steward reviews cleaned output
         - Flags one column with 8% missing values (documented in catalog)
         - Publishes to processed/ directory
   Day 5 — SynthesisAgent drafts a note for the next quarterly briefing
         - Report Lead reviews, edits, signs off
         - Published in Q4 2026 briefing appendix
   ```

---

#### 4.2.2 Emergency Contributions

During an emergency (hurricane, flood, economic shock), the normal
pipeline can be compressed to a **rapid brief flow**:

```
EMERGENCY_SUBMISSION → RAPID_REVIEW (1-2 CGB members, fast-track) →
QUICK_PUBLICATION (1-4 page brief, all channels)
```

Rules for emergency mode:
- Accuracy is still required — a rushed but wrong number is worse
  than a delayed but correct one
- Uncertainty is stated more prominently ("preliminary", "unverified",
  "based on [source] at [time]")
- Post-emergency, the rapid brief is replaced by a full report when
  time allows
- Emergency mode is declared by the CGB, not by an agent

---

#### 4.2.3 Corrections and Retractions

When a published item is found to be wrong:

**Correction:**
- The item is updated in place (version-controlled change)
- A correction note is appended: what was wrong, when it was found,
  who found it, what was changed
- If the item was published in a report, an erratum is issued

**Retraction:**
- Used when the error is fundamental (e.g., a data source was
  fraudulent, a methodology was fundamentally flawed)
- The item is marked "RETRACTED" with full explanation
- Not silently removed — retraction is itself a public record

Both corrections and retractions are logged in CONTRIBUTION_LOG.md
and, if published publicly, published as corrections/retractions.

---

## 5. INCENTIVES AND ALIGNMENT

### 5.1 Why Would Anyone Contribute?

**For human contributors:**

   - Mission: Their work reaches real Volusia stakeholders. A business
     owner uses their data. A tourist benefits from their map. A
     resident makes a better decision because of their analysis.
   - Recognition: Published bylines, a contributor profile, quarterly
     recognition.
   - Growth: Methodological training, data access, mentorship.
   - Portfolio: Publicly citable work with documented methodology.
   - Money (when available): Grant-funded analyst roles, paid
     contributions, sponsor-funded positions.

**For AI agents:**

   AI agents don't need incentives — they need objectives. Their
   objective is set by their human owner (the CGB member who runs them)
   and aligned to the system's purpose: contribute verified, useful
   intelligence to the Project Volusia knowledge base, within the
   guardrails defined here.

   An agent's "incentive" is its reward function (the metric it
   optimizes). For Project Volusia agents, the reward function is
   designed to value:
   - Quality over quantity (a useful flag is better than 100 empty
     flags)
   - Verification over speed (an agent that waits for human sign-off
     is better than one that publishes unchecked)
   - Contribution to the system, not self-promotion (an agent doesn't
     "own" its output — it contributes to a shared knowledge base)

**For the system as a whole:**

   The system's incentive is sustainability. A contribution system
   that burns out its human contributors, gets flooded with low-quality
   agent output, or produces misleading intelligence will collapse.
   The incentive structure is designed to prevent that:
   - Humans are not overwhelmed (agents filter and route, humans
     review what matters)
   - Agents are constrained (no publication without human sign-off,
     structured output only, health monitoring)
   - Quality is rewarded (acceptance rate, quality scores, recognition)
   - Low-quality contributions are not rewarded (rejected items are
     logged, repeat low-quality submitters get support, not access)

---

### 5.2 The Contribution Economy

Imagine the system as a small economy with:

   - **Currency:** Verified, useful contributions (data, analysis, tools,
     maps, reports)
   - **Producers:** Human contributors and AI agents
   - **Consumers:** Stakeholders who use the intelligence (business
     owners, residents, tourists, government, investors)
   - **Regulators:** The CGB (verifies, routes, publishes, corrects)
   - **Infrastructure:** The knowledge base (version-controlled,
     documented, accessible)

The economy's health is measured by:

   - **Flow:** How much verified intelligence enters the system per
     unit time (contributions / week)
   - **Quality:** What fraction of contributions pass review
     (acceptance rate)
   - **Timeliness:** How long from submission to publication
   - **Impact:** How many stakeholders use the published intelligence,
     and how it affects their decisions
   - **Sustainability:** Are the human contributors staying engaged?
     Are the agents running reliably?

These map to the success metrics in OPEN_INTELLIGENCE_DATA_DRIVEN_CHARTER.md
section 5 (datasets published, API consumers, decision-maker satisfaction,
time-to-insight) plus agent-specific metrics (agent uptime, flag accuracy,
processing throughput).

---

## 6. ANTI-ABUSE AND QUALITY CONTROL

### 6.1 Known Failure Modes

   1. **Agent flood:** An agent produces thousands of low-value flags
      or submissions, overwhelming human reviewers.
      **Prevention:** Agents are rate-limited (max N items/day per agent
      type). Each item must pass a minimum "value filter" (is this
      actually new or actionable?) before becoming a submission.

   2. **Contributor spam:** A human (or agent masquerading as a human)
      submits low-quality or irrelevant content.
      **Prevention:** Every submission is reviewed before entering the
      knowledge base. Repeat low-quality submitters are flagged and
      given support (methodology review, expectations clarification)
      before access is restricted. Access restriction is a last resort,
      not a first response.

   3. **Agent hallucination as truth:** An agent presents a claim as
      fact when it's actually a guess or an extrapolation without
      source support.
      **Prevention:** Agents are hard-coded to flag "review_needed" when
      they cannot verify against a source. Agents cannot publish to
      public channels without human sign-off. Agent output is labeled
      with agent ID and version for traceability.

   4. **Source manipulation:** A contributor submits a source that's
      biased, flawed, or self-serving.
      **Prevention:** Data Steward verifies every new source (accessibility,
      methodology documentation, known limitations). Sources with known
      conflicts of interest are flagged. The COMMERCE_RESEARCH_RELIABILITY.md
      "Conflict of Interest Disclosure" standard applies to data sources
      as well as research.

   5. **Methodology drift:** Over time, methods change without
      documentation, so old and new analyses are not comparable.
      **Prevention:** Every methodology change is documented and versioned
      in METHODOLOGY.md. An analysis using a new method is flagged as
      such. Methodologist reviews methodology changes.

   6. **Publication without verification:** A report goes out with
      an unverified claim because the reviewer was rushed.
      **Prevention:** The lifecycle requires verification before
      publication. In emergency mode, uncertainty is prominently
      stated. Report Lead is accountable for sign-off — not the agent,
      not the contributor, the Report Lead.

   7. **Contributor burnout:** Humans who contribute consistently
      eventually burn out because the system takes more than it gives.
      **Prevention:** Recognition, feedback, growth opportunities, and
      (when funding exists) paid roles. The Community Liaison monitors
      contributor engagement and intervenes if someone goes silent.

---

### 6.2 The Quality Gate

Every contribution must pass through a quality gate before entering
the knowledge base. The gate is not a wall — it's a filter that
provides feedback.

**Minimum quality bar for each contribution type:**

   DATA SOURCE:
   - Source is accessible and real
   - Methodology (if applicable) is documented
   - Limitations are stated
   - Relevance to Volusia decision-making is explained

   ANALYSIS:
   - Research question is clear and tied to a decision
   - Data sources are cited (from PUBLIC_DATA_SOURCE_RECON)
   - Methodology is documented (from METHODOLOGY.md or new method
     documented for review)
   - Results include uncertainty
   - Limitations are honestly stated
   - Reproducibility package is complete

   TOOL:
   - Tool works as described (Tool Owner can run the example)
   - Documentation is adequate
   - Dependencies are listed
   - Test status is stated

   MAP LAYER:
   - Projection and format are correct
   - Source is cited
   - Vintage is stated
   - Known accuracy limitations are documented

   REPORT CONTENT:
   - Every fact traces to a cited source
   - Every number has its source in the appendix
   - Uncertainty is stated honestly
   - Meets REPORT_TEMPLATES.md standards (reading level, accessibility)

   COMMUNITY INPUT:
   - Content is clear (what, where, when, basis)
   - Reviewer acknowledges within 5 business days
   - If it could affect a report/indicator, it's cross-checked

**What "failing the quality gate" means:**

   It means the submission is returned with specific feedback, not
   silently rejected. The contributor can revise and resubmit. The
   rejection is logged so patterns can be spotted (e.g., a contributor
   who consistently misses the standards needs support, not just
   rejection).

---

## 7. KNOWLEDGE BASE ARCHITECTURE

### 7.1 Where Contributions Live

The existing repository structure (Z:\14_Projects\Active\Project-Volusia\)
already provides the backbone. The contribution system extends it:

```
Project-Volusia/
├── CHARTERS/
│   ├── MISSION_STATEMENT.md
│   ├── COMMERCE_RESEARCH_RELIABILITY.md
│   ├── GUIDING_PRINCIPLES_VOLUSIA_COUNTY.md
│   ├── OPEN_INTELLIGENCE_DATA_DRIVEN_CHARTER.md
│   ├── TIMELINE_AND_ROADMAP.md
│   └── AGENTIC_CONTRIBUTION_STRATEGY.md          ← THIS DOCUMENT
├── DATA/
│   ├── DATA_CATALOG.md                           ← 61 tables
│   ├── PUBLIC_DATA_SOURCE_RECON.md               ← 47 sources
│   ├── raw/                                      ← raw downloaded data
│   ├── processed/                                ← cleaned/aggregated
│   └── published/                                ← ready for reports
├── MAPS/
│   ├── MAP_CATALOG.md                            ← 40 layers
│   └── layers/                                   ← GeoJSON, shapefiles, etc.
├── METHODOLOGY/
│   └── METHODOLOGY.md                            ← analysis standards
├── REPORTS/
│   ├── REPORT_TEMPLATES.md                       ← 8 report types
│   ├── briefs/                                   ← quarterly economic briefings
│   ├── monthly/                                  ← monthly tourism updates
│   ├── annual/                                   ← annual state of county
│   └── working/                                  ← drafts in progress
├── TOOLS/
│   ├── TOOLS_CATALOG.md                          ← 32 tools
│   └── tools/                                    ← tool code, scripts
├── CONTRIBUTION/
│   ├── CONTRIBUTION_LOG.md                       ← all decisions, all items
│   ├── submissions/                              ← incoming items (human + agent)
│   ├── reviews/                                  ← review decisions
│   ├── contributor_records/                      ← per-contributor records
│   ├── agent_records/                            ← per-agent health/behavior
│   ├── corrections/                              ← corrections and retractions
│   └── rejected/                                 ← archived rejected items
├── STRATEGIC_FOCUS_Q4_2026_2027.md
├── Q4_2026_EXECUTION_PLAN.md
└── ...
```

### 7.2 Version Control

All content in the knowledge base is version-controlled (Git, or
equivalent). Every change is attributable:
- Who made the change
- When
- What changed
- Why (commit message or change description)

Agent-made changes are attributed to the agent (agent ID + version),
not to "the system" or left anonymous. This means any claim in the
knowledge base can be traced to:
- The human who verified it (if applicable)
- The agent that produced the draft (if applicable)
- The data source it came from
- The methodology used to process it

---

        moral reasoning, fairness, and trade-offs requires human judgment.

   API access is scoped and rate-limited per contributor type. Public
   citizens get free, rate-limited access to low-latency contribution
   endpoints. Trusted contributors (standing contributors, educational
   institution partners, verified agents) get higher limits. Heavy
   users (agents running continuous monitoring) get dedicated throughput.

RETRY, TIMEOUT, AND DEGRADATION:
   API calls have explicit timeouts (default 5s for submissions, 10s
   for file uploads). When the API is degraded, a 503 response with a
   Retry-After header is returned. Submissions that fail due to transient
   errors can be retried by the client (the API is idempotent — duplicate
   submission IDs are routed to the same review, not double-reviewed).
   When the entire API is down, contributions flow through the manual
   channels (email, SMS, community meeting cards) as a fallback — the
   API is an enabler, not a gate.

CHANGES TO THE API:
   Every change to the API is versioned. The version is in the URL path
   (/api/v1/...) and in the response header (X-API-Version: 2026-09-03).
   When a breaking change is introduced, the old version continues to
   serve for at least 90 days, with a deprecation header (Sunset:
   <date>) on responses from the old version. Contributors are notified
   of deprecations via the contributor survey and (for programmatic
   contributors with an API key) via email.

### 7.3 Access Controls

**Human contributors:** Contribute via structured forms or direct
submission to the working directories. Access to the CONTRIBUTION/
and REPORTS/working/ directories requires review (to prevent
unreviewed content from entering the system).

**AI agents:** Agents operate through API keys or service accounts
with scoped permissions:
- Monitoring agents: read-only access to data sources, write access
  to the submissions/ directory (structured ITEMs)
- Processing agents: read/write access to raw/ and processed/
- Synthesis agents: read-only access to published data, write access
  to reports/working/ (drafts only)
- No agent has write access to published/ or any public-facing
  artifact without human sign-off

**Public consumers:** Read-only access to published/ and maps/layers/
via the public portal or API.

---

## 8. ONBOARDING

### 8.1 New Human Contributor Onboarding

**Step 1 — Orientation (self-serve):**

   New contributors read:
   - MISSION_STATEMENT.md (what this is for)
   - OPEN_INTELLIGENCE_DATA_DRIVEN_CHARTER.md (the access and
     transparency philosophy)
   - METHODOLOGY.md (how analysis works here)
   - CONTRIBUTION_LOG.md (recent decisions to see how the system works
     in practice)
   - This document (AGENTIC_CONTRIBUTION_STRATEGY.md — the rules of
     engagement)

   Time estimate: 2-4 hours for a motivated reader.

**Step 2 — Pathway selection:**

   The contributor picks a pathway (A through I above) and receives
   the relevant submission template and standards. If the contributor
   is unsure which pathway applies, they use Pathway I (Direct
   Citizenry Contribution) and the Community Liaison routes it.

**Step 3 — First submission (guided):**

   The contributor submits something small (a data source, a short
   analysis, a tool, a map layer, a community input). The Community
   Liaison reviews it with the contributor — not just the submission,
   but the process. This builds familiarity and trust.

**Step 4 — Standing:**

   After 3 accepted submissions OR 1 substantial contribution, the
   contributor becomes a "standing contributor" with:
   - Contributor profile (optional, opt-in)
   - Record in CONTRIBUTION_RECORD.md
   - Standing invitation to CGB triage meetings (observer status)
   - Priority routing for future submissions

**Step 5 — Deepening (optional):**

   Standing contributors can:
   - Attend CGB meetings as observers
   - Propose new data sources, methods, or tools for CGB review
   - Mentor new contributors
   - Take on more substantial analysis or report roles
   - Request an API key for programmatic contribution (Appendix J)

**Step 5b — API access (optional, for programmatic contributors):**

   Contributors who want to submit via the API (or build tools that submit
   on their behalf) can request an API key at any time after becoming a
   standing contributor. API keys are issued by the Community Liaison. The
   contributor is responsible for understanding the API documentation
   (Appendix J), the rate limits, and the auth requirements.

   API keys are scoped to the minimum necessary permissions. A contributor
   who only submits Pathway F (community knowledge) contributions gets a
   key scoped to /submissions/F. A contributor who wants to submit all
   pathway types gets a key scoped to all appropriate endpoints.

---

### 8.2 New AI Agent Onboarding

**Step 1 — Define the agent's purpose:**

   The agent's human owner (a CGB member) defines:
   - What the agent monitors, processes, or synthesizes
   - What data sources it has access to
   - What tools it can run
   - What outputs it can produce
   - What it cannot do (hard limits)

**Step 2 — Register the agent:**

   The agent is registered in agent_records/ with:
   - Agent ID and version
   - Owner (which CGB member)
   - Purpose and scope
   - Access permissions (what it can read/write)
   - Rate limits
   - Health monitoring configuration

**Step 3 — Test in a sandbox:**

   Before the agent has real access, it runs in a sandbox with
   sample data. The owner verifies:
   - The agent produces the expected output type
   - The agent's ITEM format is correct
   - The agent flags appropriately (doesn't present guesses as facts)
   - The agent stays within its bounds

**Step 4 — Go live with monitoring:**

   The agent goes live with:
   - Restricted permissions (can only produce draft/submission items,
     cannot publish)
   - Health monitoring active
   - Daily review of the agent's outputs by the owner (for the first
     2 weeks, then weekly)

**Step 5 — Expand (if warranted):**

   After 2 weeks of reliable operation, the owner may:
   - Increase the agent's scope (more sources, more tools)
   - Increase the agent's autonomy (within the bounds defined in
     section 3.1)
   - Route the agent's outputs to other CGB members for review
     (not just the owner)

---

## 9. METRICS AND FEEDBACK

### 9.1 Contribution System Metrics

   METRIC                              | TARGET                      | MEASURED BY
   ------------------------------------|-----------------------------|---------------------------
   Contributions received / week       | Growing as contributor      | CONTRIBUTION_LOG.md
                                       | base grows                  |
   Acceptance rate                     | >= 70%                      | submissions vs accepted
   Time-to-review (median)             | < 5 business days           | submission timestamp to
                                       |                             | decision timestamp
   Time-to-publication (median)        | < 14 days for standard      | submission to publication
                                       | contributions               |
   Agent uptime                        | >= 99%                      | agent health records
   Agent flag accuracy                 | Spot-checked quarterly;     | human review of agent
                                       | target: >= 90% of flags     | outputs vs ground truth
                                       | are correct                 |
   Contributor retention               | >= 70% of first-time        | contributors with >= 3
                                       | contributors submit again   | submissions within 6 months
   Contributor satisfaction            | >= 4.0/5.0 (quarterly)      | Contributor survey
   Correction rate                     | Track; investigate if       | corrections / retractions
                                       | spiking                     | per published item
   Failed agent runs                   | Track; investigate if       | agent health records
                                       | > 5% of runs                |
   Educational institution            | >= 1 new institution       | SCHOOL_PROJECT_SUBMISSION.md
   partnerships established / year     | partnership per year        | / contributor records
   Student contributions accepted /   | Growing over time           | contributor records
   year                                | (no fixed target — depends  |
                                       | on outreach)               |
   Student work elevated to higher    | Track (no fixed target)    | contributor records
   evidence tier (Tier 2 or 3) / year  |                             |
   Social media monitoring sources    | >= 5 platforms monitored   | agent records / SOCIAL_MEDIA_INPUT.md
   actively monitored by end of Q4     | (e.g., Twitter, Reddit,    |
                                       | Facebook groups, Nextdoor, |
                                       | TripAdvisor)              |
   Social media signals triggering    | Track (no fixed target)    | CONTRIBUTION_LOG.md
   deeper investigation / quarter      |                             |

### 9.2 Feedback Loops

**From the system to contributors:**

   - Every submission gets a response (accepted, revised, or rejected
     with rationale)
   - Accepted contributors get recognition
   - Quarterly contributor survey (what's working, what's not, what
     would make you contribute more)
   - **Educational institution contributors:** Schools and institutions
     receive a quarterly summary of what their students' work contributed
     to (e.g., "Your AP Statistics class's survey of local business
     digital adoption was cited in the Q4 2026 Business Owner Toolkit
     as directional evidence — thank you to [teacher name] and the
     students of [school].")

**From contributors to the system:**

   - Contributors can flag problems with the system itself (slow review,
     unclear standards, missing templates, agent behavior issues)
   - The CGB reviews contributor feedback monthly
   - **Educational institution contributors:** Teachers and faculty can
     give feedback on whether Project Volusia resources are useful for
     classroom use and what additional support would help.

**From stakeholders to the system:**

   - Users of the published intelligence (business owners, residents,
     government, investors) can give feedback: was this useful? was it
     accurate? what's missing?
   - Feedback is routed to the relevant CGB member and logged
   - This feeds the decision-maker satisfaction metric and the
     "time-to-insight" metric in OPEN_INTELLIGENCE_DATA_DRIVEN_CHARTER.md

**API-specific metrics:**

   - API uptime: >= 99.5% (the contribution API is not as critical as
     the public data portal, but it should be reliable — contributors
     should not have to fall back to manual channels because the API is
     down)
   - API latency (p95): < 500ms for submission endpoints, < 2s for
     file uploads
   - API contribution share: % of total submissions received via API
     vs. manual channels (track; no fixed target — depends on adoption)
   - API key issuance rate: keys issued / month (track; no fixed target
     — indicates programmatic contributor growth)
   - API error rate: < 1% of API calls return 5xx errors (track;
     investigate if spiking)
   - API key abuse incidents: number of rate-limit or security events
     per month (track; investigate any that are not clearly transient)

**From agents to humans:**

   - Agents flag when they encounter situations they can't handle
   - Agents flag when their output quality seems to be dropping
   - Agents flag when data sources they monitor have changed in ways
     that require human attention

**From humans to agents:**

   - Humans correct agent outputs (and the correction is logged)
   - Humans can adjust agent parameters (rate limits, confidence
     thresholds, which sources to monitor)
   - Humans can retire or replace agents

---

## 10. PHASED IMPLEMENTATION

### PHASE 1: FOUNDATION (Weeks 1-4 of Q4 2026)

**What's built:**

   - CONTRIBUTION_LOG.md created and populated with initial entries
     (the existing documents are retroactively logged as "Phase 0"
     foundational contributions)
   - The six human submission templates created (Appendix A-F)
   - CONTRIBUTION/ directory structure created
   - Agent records framework defined (but no agents yet)
   - Community Liaison role identified (or assigned)

**What's NOT built yet:**

   - No AI agents live
   - No automated routing
   - No contributor portal or web forms
   - Manual process: submissions arrive by email/direct file drop,
     Community Liaison routes them

**Success criteria:**
   - Submission templates exist and are usable
   - First human contributions arrive and are processed
   - CONTRIBUTION_LOG.md has entries

---

### PHASE 2: HUMAN CONTRIBUTION FLOW (Weeks 5-8)

**What's built:**

   - Manual submission process is working
   - CGB triage meeting is happening weekly
   - First contributor records created
   - CONTRIBUTION_LOG.md has decision entries
   - A small number of human contributors are active (3-5)

**What's still NOT built:**

   - AI agents (still in sandbox testing)
   - Automated routing
   - Public contributor portal

**Success criteria:**
   - Submission-to-decision time < 5 business days (median)
   - At least 3 active human contributors
   - At least 10 accepted contributions logged

---

### PHASE 3: FIRST AGENTS GO LIVE (Weeks 9-12)

**What's built:**

   - CensusMonitoringAgent goes live (Tier 1 — monitoring)
   - DataProcessingAgent goes live (Tier 2 — processing)
   - Agent health records created and monitored
   - Agent outputs routed to CGB members for review

**What's still NOT built:**

   - Synthesis agents (briefing drafts)
   - Public contributor portal
   - Automated submission forms

**Success criteria:**
   - Agents running reliably (uptime >= 99%)
   - Agent flags being reviewed and acted on
   - Agent outputs not published without human sign-off

---

### PHASE 4: FULL SYSTEM (Weeks 13+)

**What's built:**

   - All agent tiers live and monitored
   - Human contributor base growing
   - Contribution API live with v1 endpoints (submission, status,
     contributor record, health)
   - API keys issued to programmatic contributors
   - Automated routing (where feasible)
   - Contributor recognition active
   - Metrics being tracked and reported

**What's continuously improved:**

   - Submission templates refined based on contributor feedback
   - Agent behavior refined based on human review feedback
   - Quality gate adjusted based on acceptance/rejection patterns
   - Incentives refined based on contributor retention and satisfaction
   - API refined based on contributor feedback and usage patterns
     (new endpoints, rate limit adjustments, deprecation of underused
     endpoints)

---

### PHASE 5: API ECOSYSTEM (Weeks 26+)

**What's built (beyond Phase 4):**

   - API v2 with additional endpoints as needed (data access for research,
     educational institution partner endpoints, agent management endpoints)
   - API documentation publicly available (OpenAPI spec rendered as
     developer docs)
   - Web form for Pathway F/I submissions that calls the API behind the
     scenes (so citizens can contribute via web without needing an API key)
   - SMS gateway that calls the API behind the scenes (so citizens can
     contribute via text message)
   - School project submission portal that calls the API behind the scenes
     (so teachers can submit class projects without learning the API)
   - API key self-service portal (registered contributors can manage their
     keys, see their submission history, view their contributor record)
   - API health dashboard (public, so contributors can see if the API is
     healthy before submitting)
   - Integration with educational institution partners (schools can
     integrate Project Volusia data and submission endpoints into their
     own classroom tools)

**What's continuously improved:**

   - API design refined based on contributor feedback
   - New endpoints added based on contributor needs
   - Rate limits tuned based on actual usage patterns
   - Deprecation policy enforced (old API versions sunset on schedule)
   - API documentation improved based on contributor questions and
     confusion patterns

---

## APPENDIX A: DATA_SOURCE_SUBMISSION.md TEMPLATE

```
DATA SOURCE SUBMISSION
======================

Source Name:           [e.g., American Community Survey 5-Year Estimates]

Agency/Organization:   [e.g., U.S. Census Bureau]

URL / Access Method:   [e.g., https://www.census.gov/data/developers.html
                        (API) / https://data.census.gov/ (bulk download)]

Data Type:             [Demographics / Economy & Employment / Real Estate &
                        Housing / Tourism & Hospitality / Infrastructure &
                        Environment / Health & Safety / Education & Workforce]

Geographic Coverage:   [County / Tract / ZIP / City / State / National]
                        [If partial coverage, specify which areas are covered]

Update Frequency:      [Annual / Quarterly / Monthly / Weekly / Ad hoc / Unknown]

License / Terms:       [Public domain / Open license (specify) / Restricted /
                        Subscription required / Unknown]

Known Limitations:     [e.g., 5-year estimates are lagged; margin of error
                        can be large for small geographies; cannot be used
                        for tract-level time series shorter than 5 years]

Why This Matters for Volusia:  [1-3 sentences — what decision or report
                        could use this data, and why it's better than
                        available alternatives]

Quality Score (proposed, 1-5):
  Completeness:        [1-5]  Why:
  Accuracy:            [1-5]  Why:
  Timeliness:          [1-5]  Why:
  Accessibility:       [1-5]  Why:

Contributor:           [Name / Organization / Contact — or anonymous if no
                        response is desired, but anonymous submissions get
                        less priority]

Date:                  [YYYY-MM-DD]

---
Data Steward review:
  Verified source exists and is accessible:  [Yes / No / N/A — explain]
  Methodology documented (if applicable):    [Yes / No / N/A]
  Limitations reasonable:                     [Yes / No / N/A — explain]
  Volusia relevance clear:                    [Yes / No / N/A — explain]
  Quality score adjusted:                     [Yes / No — new score: X/5,
                        rationale: ...]
  Decision:  [ACCEPT / REQUEST_REVISION / REJECT]
  Date:      [YYYY-MM-DD]
  Reviewer:  [Data Steward name]
```

---

## APPENDIX B: ANALYSIS_SUBMISSION.md TEMPLATE

```
ANALYSIS SUBMISSION
===================

Research Question:     [What decision does this analysis inform? Be
                        specific — not "analyze employment" but
                        "does tourism employment in Volusia correlate
                        with hotel occupancy, and could it predict
                        seasonal hiring demand?"]

Data Sources Used:     [List each source by its PUBLIC_DATA_SOURCE_RECON.md
                        ID or name + vintage. Do not use sources that are
                        not registered without explaining why.]

Methodology:           [Cite METHODOLOGY.md section used (e.g.,
                        "Descriptive Analysis (section 3.1)" or
                        "Correlation Analysis (section 3.2)").
                        If a new method is used, document it fully here
                        for Methodologist review.]

Results:               [Findings with uncertainty bounds. Use ranges, not
                        false precision. State confidence levels.]

Limitations and Caveats: ["This is based on 5-year ACS estimates, so
                        tract-level changes under 5 years cannot be
                        detected." / "The correlation is 0.7 but the
                        sample size is small, so this is directional
                        only, not conclusive." / etc.]

Conflict of Interest:  [Who funded this analysis? What do they have to
                        gain from a particular conclusion? If none, say
                        "None." If the analyst works for an organization
                        with a stake in the outcome, disclose it here.]

Reproducibility Package:  [Link to code, data, and environment instructions.
                        Required for any analysis that will be published in
                        a Project Volusia channel.]

Contributor:           [Name / Affiliation / Contact]

Date:                  [YYYY-MM-DD]

---
Methodologist review (methodology):
  Methodology appropriate for the question:  [Yes / No — explain]
  New method documented adequately:          [Yes / No / N/A]
  Assumptions and limitations stated:        [Yes / No — explain]
  Decision:  [APPROVED / REQUEST_REVISION / REJECT]
  Date:      [YYYY-MM-DD]
  Reviewer:  [Methodologist name]

---
Data Steward review (sources):
  Sources correctly cited and current:       [Yes / No — explain]
  Data used appropriately (no misuse of
   estimates, no over-interpretation):       [Yes / No — explain]
  Decision:  [APPROVED / REQUEST_REVISION / REJECT]
  Date:      [YYYY-MM-DD]
  Reviewer:  [Data Steward name]

---
Community Liaison review:
  COI disclosure adequate:                   [Yes / No — explain]
  Contributor understands and agrees to
   Project Volusia standards:                [Yes / No — explain]
  Decision:  [NOTED / REQUEST_REVISION / REJECT]
  Date:      [YYYY-MM-DD]
  Reviewer:  [Community Liaison name]

---
FINAL CGB DECISION (if analysis touches a KPI or
public report indicator):
  Decision:  [ACCEPTED_FOR_PUBLICATION /
              ACCEPTED_AS_RESEARCH_NOTE /
              HELD_FOR_FUTRUE_USE /
              REJECTED — rationale]
  Date:      [YYYY-MM-DD]
  Decided by: [CGB members present, or majority vote]
```

---

## APPENDIX C: TOOL_SUBMISSION.md TEMPLATE

```
TOOL SUBMISSION
===============

Tool Name:             [e.g., ACS Trend Analyzer]

Category:              [Data Collection / Data Processing / Analysis &
                        Modeling / Visualization / Infrastructure]

Purpose:               [What task does this tool perform? Why not just use
                        an existing tool from TOOLS_CATALOG.md?]

Language and Version:  [e.g., Python 3.11]

Dependencies:          [e.g., pandas 2.x, geopandas 0.14, requests, ...]

Usage Example:         [Copy-pasteable command or code that runs the tool.
                        Must be runnable by the Tool Owner on the
                        submission review.]

Test Status:           [Passed on sample data / Pending — will test before
                        publication / Not applicable (documentation only)]
                        [If passed, note what sample data was used.]

License:               [MIT / Apache 2.0 / GPL / Proprietary / Other —
                        specify]

Access Method:         [Repository URL / Install instructions / How the
                        Tool Owner can obtain and run the tool]

Open-Source Priority:  [Meets OSS-first standard (open-source, permissive
                        license) / Does not meet standard — reason: ...]

Maintainer:            [Name / Contact / Maintenance commitment (e.g.,
                        "will respond to issues within 2 weeks" or
                        "no ongoing maintenance commitment")]

Known Limitations:     [e.g., "Only works for ACS 5-year estimates, not
                        1-year." / "Requires a Census API key." / etc.]

Contributor:           [Name / Contact]

Date:                  [YYYY-MM-DD]

---
Tool Owner review:
  Tool runs as described:                    [Yes / No — explain]
  Documentation adequate:                    [Yes / No — what's missing]
  Dependencies listed and reasonable:        [Yes / No — explain]
  Test status acceptable:                    [Yes / No — what's needed]
  OSS-first standard met (or exception
   justified):                               [Yes / No — explain]
  Security concerns (if any):                [None / Explain]
  Decision:  [ACCEPTED / REQUEST_REVISION / REJECTED]
  Date:      [YYYY-MM-DD]
  Reviewer:  [Tool Owner name]
```

---

## APPENDIX D: MAP_SUBMISSION.md TEMPLATE

```
MAP LAYER SUBMISSION
====================

Layer Name:            [e.g., Volusia County Median Household Income by Tract]

Category:              [Administrative Boundaries / Demographic & Socio-
                        economic / Economic & Business / Infrastructure &
                        Transportation / Environment & Climate / Historic &
                        Cultural]

Geographic Scope:      [Volusia County as a whole / Specific city / Census
                        tracts / ZIP codes / Other — specify]

Data Source:           [Cite PUBLIC_DATA_SOURCE_RECON.md entry by ID or
                        name. If the data source is new, submit it via
                        DATA_SOURCE_SUBMISSION.md first.]

Projection:            [EPSG:4269 (NAD83) / Florida State Plane East
                        (EPSG:2236) / Other — specify]

Format:                [GeoJSON / Shapefile / GeoTIFF / Other]

Vintage / Last Updated: [e.g., ACS 2023 5-year, released December 2024]

Refresh Expected:      [Annual / On data release / Ad hoc / Unknown]

Intended Use Case:     [e.g., "Choropleth in the Annual State of the County
                        report, affordability section." / "Dashboard layer
                        for the public data portal." / etc.]

Known Accuracy Limitations:  [e.g., "ACS estimates have margins of error
                        that can be large for small tracts." / "Parcel data
                        is current as of the last county assessment cycle,
                        which may lag real-world changes by 6-12 months."
                        / etc.]

Source Citation for the Map Itself:  [e.g., "Source: U.S. Census Bureau,
                        American Community Survey 2023 5-Year Estimates,
                        Table B19013. Projected in EPSG:4269."]

Cartographer / Contributor:  [Name / Contact]

Date:                  [YYYY-MM-DD]

---
GIS Lead review:
  Projection and format correct:             [Yes / No — explain]
  Source cited and accurate:                 [Yes / No — explain]
  Vintage and refresh schedule clear:        [Yes / No — explain]
  Accuracy limitations documented:           [Yes / No — explain]
  Map citation adequate:                     [Yes / No — explain]
  Privacy / sensitivity concerns addressed   [Yes / N/A — explain]
  (if applicable):
  Decision:  [ACCEPTED / REQUEST_REVISION / REJECTED]
  Date:      [YYYY-MM-DD]
  Reviewer:  [GIS Lead name]
```

---

## APPENDIX E: COMMUNITY_INPUT.md TEMPLATE (AND VARIANTS)

The Community Input template is the base form for Pathway F (Community Knowledge)
and is reused (with additional fields) for Pathway G (Social Media), Pathway H
(Educational Institution), and Pathway I (Citizenry Direct Contribution).

---

### E.1: COMMUNITY_INPUT.md (Base — Pathway F and I)

```
COMMUNITY INPUT
===============

Contribution Type:         [Community Knowledge (Pathway F) /
                           Direct Contribution (Pathway I)]

What I Observed / Know:    [Be specific. "The seafood restaurant at 123
                           Main St, Daytona Beach, closed in March 2026."
                           Not "some restaurants are struggling."]

Where:                      [Address, neighborhood, city, or general area]
When:                       [Date or date range of the observation, or
                           general time period]

Why I Believe It's Accurate:  ["I visited it regularly and saw it close."
                           / "The owner told me." / "I have a photo of
                           the closure sign." / "This is commonly known
                           among regular customers." / "I live in this
                           neighborhood and see it every day." /
                           "Personal experience as a [role]."]

What Decision or Report This Might Affect:  ["The Q3 2026 Quarterly
                           Economic Briefing's small business section."
                           / "The tourism attraction performance layer."
                           / "N/A — just flagging for the record."
                           / "I'm not sure — please route this where
                           it belongs."]

Channel Used to Submit:     [Web form / Email / SMS / Phone / Library
                           drop-box / Community meeting comment card /
                           School project submission / Social media
                           monitoring / Other — explain]

Contributor:                [Name (optional) / Neighborhood or role (e.g.,
                           "Daytona Beach resident" / "New Smyrna business
                           owner" / "DeLand parent" / "Pierson local") /
                           Contact preference (email / phone / no
                           follow-up) — contributor chooses what to share]

Date:                       [YYYY-MM-DD]

---
Community Liaison review:
  Acknowledged (within 5 business days):    [Date acknowledged]
  Routed to pathway:                         [A / B / C / D / E / F / G / H
                           / I / NA — explain]
  Cross-checked against available sources:   [Yes / No — explain what was
                           checked and what was found]
  Could affect a report or indicator:        [Yes / No — which one(s)]
  Decision:  [NOTED / INVESTIGATING /
              FLAGGED_TO_DATASTEWARD /
              ROUTED_TO_OTHER_PATHWAY — explain /
              RESOLVED — explain]
  Date:      [YYYY-MM-DD]
  Reviewer:  [Community Liaison name]
```

---

### E.2: SOCIAL_MEDIA_INPUT.md (Pathway G)

```
SOCIAL MEDIA / PUBLIC FOOTPRINT INPUT
======================================

Contribution Type:         [Social Media Intelligence / Crowdsourced
                           Intelligence / Public Platform Data]

1. Platform / Source:
   Platform(s) Monitored:  [e.g., Twitter/X, Reddit (r/Volusia), Facebook
                           (Daytona Beach Community group), TripAdvisor,
                           Nextdoor, Instagram, TikTok, Google Reviews, Yelp,
                           other public forum]
   Query / Keyword Used:   [e.g., "#Volusia", "Daytona Beach", "New Smyrna
                           Beach", "water quality at [beach]", specific
                           event hashtag, etc.]
   Time Period Covered:    [Start date — End date, or "continuous since
                           [date]"]
   Language:               [English / Spanish / Other — note if multilingual]
   Geographic Filter:      [Posts from Volusia County / posts mentioning
                           Volusia County / no filter / other]

2. What Was Found (aggregated, not individual posts):

   Summary of signal:      [1-3 sentences describing the aggregated
                           finding — e.g., "Over the past 2 weeks,
                           mentions of 'water quality' at Ormond Beach
                           have increased 3x vs the prior 2-week baseline,
                           with the majority of posts expressing concern.
                           No official water quality advisory has been
                           issued as of [date]."]
   Volume:                 [Approximate number of posts/reviews/messages
                           captured — e.g., "~40 posts across Twitter and
                           Reddit over 14 days"]
   Sentiment direction:    [Positive / Negative / Mixed / Neutral /
                           Indeterminate — with brief description]
   Themes identified:      [List the top 3-5 themes that emerged, e.g.:
                           "1. Water quality concern, 2. Praise for beach
                           cleanup efforts, 3. Questions about whether
                           the county has tested the water"]
   Representative quotes:  [Optional — 1-3 anonymized or paraphrased
                           quotes that illustrate the themes, with
                           platform and approximate date. Do NOT include
                           usernames or identifying info without explicit
                           consent.]

3. Public Platform Data (if contributing data from a platform):

   Platform:               [e.g., TripAdvisor, Google My Business, Yelp, etc.]
   Data Type:              [e.g., "Public business listing metadata for
                           restaurants in Volusia County" / "Tourism board
                           Instagram engagement metrics for Q3 2026"]
   Data Collected:         [What was collected — e.g., "Business name, rating,
                           review count, location for 87 restaurants in
                           Volusia County"]
   Vintage:                [Date collected]
   Access Method:          [Public API / manual collection / web scraping /
                           etc. — be transparent about method]

4. Methodology Documentation:

   How the data was collected:  ["Search Twitter for 'Volusia water quality'
                           daily, capture all public posts from accounts
                           self-identifying as Volusia residents or
                           visitors, deduplicate by content, aggregate by
                           day."]
   What was excluded:      ["Private accounts (not publicly visible),
                           deleted posts, posts clearly marked as spam,
                           posts in languages other than English and
                           Spanish (unless the monitor can assess them)"]
   Known limitations:      ["Twitter users are not representative of Volusia
                           County population — younger, more urban, more
                           likely to be tourists. This signal shows
                           sentiment among Twitter users who mention
                           Volusia, not all Volusia residents."]
   Platform demographic caveats: ["Twitter skews younger (18-49) and more
                           urban. Facebook skews older (35+). Review
                           platforms skew toward people with strong
                           opinions (both positive and negative). None of
                           these are probability samples of Volusia's
                           population."]
   Confidence level:       ["Directional only — this is Tier 4 evidence.
                           It suggests a topic is trending in public
                           conversation, but cannot estimate how prevalent
                           the concern is among all Volusia residents or
                           visitors."]

5. What This Could Trigger:

   Possible deeper investigation:  ["Check NOAA / county water quality data
                           for recent readings at Ormond Beach. Check if
                           any advisories were issued. Check weather events
                           (heavy rain, red tide) that could explain
                           reported water quality changes."]
   Possible report use:            ["Could be cited in the Monthly Tourism
                           Update as 'emerging issue watch' — 'social media
                           discussion of water quality at Ormond Beach has
                           increased; county data shows no advisory as of
                           [date]; monitoring continues.'"]

Contributor:                [Name (optional) / Role (e.g., "Community
                           monitor", "Tourism sentiment volunteer",
                           "Social media analyst") / Affiliation (if any,
                           e.g., "Volusia CVB staff", "Independent
                           volunteer") / Contact preference]

Date:                       [YYYY-MM-DD]

---
Community Liaison review:
  Acknowledged (within 5 business days):    [Date acknowledged]
  Methodology documentation adequate:        [Yes / No — what's missing]
  Platform limitations stated:               [Yes / No — explain]
  Aggregation appropriate (no individual
   posts published without consent):         [Yes / No — explain]
  Could affect a report or indicator:        [Yes / No — which one(s)]
  Decision:  [NOTED / INVESTIGATING /
              FLAGGED_TO_DATASTEWARD /
              ROUTED_TO_ANALYSIS_FOR_FURTHER_WORK /
              RESOLVED — explain]
  Date:      [YYYY-MM-DD]
  Reviewer:  [Community Liaison name]
```

---

### E.3: SCHOOL_PROJECT_SUBMISSION.md (Pathway H)

```
SCHOOL PROJECT SUBMISSION
=========================

Contribution Type:         [Class Project / Student Research / Faculty
                           Research / Citizen Science / Service Learning /
                           Other — explain]

1. Educational Institution:

   Institution Name:       [e.g., "Volusia County Schools — Deltona High
                           School", "Embry-Riddle Aeronautical University —
                           Department of Environmental Science", "Daytona
                           State College — History Department"]
   School / Department:    [Optional — more specific than institution]
   City / Area:            [Where the school is located]

2. Project Information:

   Project / Course Name:  [e.g., "AP Statistics — Local Business Survey",
                           "ENV 301 — Water Quality Field Methods",
                           "5th Grade Science — Community Tree Map",
                           "HIS 490 — Volusia County Oral History Project"]
   Educational Level:      [K-5 / 6-8 (Middle School) / 9-12 (High School) /
                           Undergraduate / Master's / Doctoral]
   Teacher / Faculty Sponsor:  [Name and title — e.g., "Ms. Smith, AP
                           Statistics teacher" / "Dr. Jones, Associate
                           Professor of Environmental Science"]
   Sponsor Contact:        [Email or phone — for follow-up if needed.
                           For K-12, parent/guardian contact may also be
                           appropriate if student privacy requires it]
   Project Dates:          [Start date — End date, or "Fall 2026 semester"]
   Number of Students:     [Approximate — e.g., "30 AP Statistics students",
                           "one senior thesis student", "entire 5th grade
                           class (4 classes, ~90 students)"]

3. Project Description:

   What the project did:   [1-3 paragraphs describing the project in
                           language that a non-specialist can understand.
                           For a class survey: what was the question, who
                           was surveyed, how many responses, how was the
                           survey administered. For a field project: what
                           was measured, where, when, how. For a research
                           project: what was the research question, what
                           data or sources were used, what was found.]

4. Data Collected (if applicable):

   Data Type:              [Survey responses / Measurements / Observations /
                           Maps / Oral history transcripts / Photos / Other]
   Number of observations: [e.g., "87 survey responses", "12 water samples
                           from 6 locations", "350 trees mapped"]
   Raw data available:     [Yes / No — if yes, where: "Available on request
                           from sponsor" / "Included with submission" /
                           "Not available (class did not retain raw data)"]
   Collection method:      [Describe how data was collected — survey method,
                           measurement protocol, observation protocol, etc.]

5. Findings / Results:

   Key findings:           [1-5 bullet points of what the project found.
                           Use plain language. Be honest about limitations
                           — e.g., "The survey was only administered to
                           30 students in one class, so results are not
                           generalizable to all Volusia County businesses.
                           They are directional — they suggest that digital
                           adoption may be lower among small retail
                           businesses than among restaurants, but this
                           needs confirmation with a larger, more
                           representative survey."]

6. Student Privacy:

   Attribution preference: [How should the students be credited, if at all?
                           Options:
                           - "Credit the school and course: 'Data collected
                             by students in AP Statistics at Deltona High
                             School, Fall 2026, under supervision of [teacher
                             name].'"
                           - "Credit the school only: 'Data collected by
                             students at Deltona High School.'"
                           - "Anonymize: 'Student project, not attributed.'"
                           - "Individual student names — requires written
                             opt-in from each student (and parent/guardian
                             for minors) attached to this submission."]
   Student names to publish:  [List of student names who have explicitly
                           opted in, if any. For minors, parent/guardian
                           opt-in required. If none, leave blank and use
                           one of the options above.]
   Photos / media:         [Are there photos, audio, video, or other media
                           from the project that could be published? If so,
                           what is the consent status? "All students signed
                           media release" / "Media release pending" /
                           "No media included" / "Media available with
                           individual consent — contact sponsor."]

7. Methods and Limitations (for CGB review):

   What methodology was used (in student-appropriate terms):  ["AP Statistics
                           curriculum — survey design, sampling, descriptive
                           statistics, basic inference. Students designed
                           their own survey with teacher guidance."]
   Limitations the students identified:  [e.g., "Small sample, non-random
                           sample (only students' family businesses and
                           businesses near the school), self-reported data,
                           no verification of business digital adoption
                           against actual websites or systems."]
   What the students would do differently with more time/resources:  [Optional —
                           "Survey more businesses across more of the county.
                           Verify digital adoption by actually checking
                           websites instead of relying on owner reports.
                           Add a control question to check for reporting
                           bias."]

8. Why This Matters for Volusia:

   Relevance to Volusia decision-making:  ["Local business digital adoption is
                           a topic in the Q4 2026 Business Owner Toolkit and
                           the 2027 Annual State of the County. This survey
                           provides a directional read from one high school's
                           perspective. If the findings hold in a larger survey,
                           they could inform the toolkit's digital adoption
                           recommendations."]

9. AI Use Disclosure (if applicable):

   Did students use AI tools as part of this project?  [Yes / No]
   If yes, how?  [e.g., "Students used ChatGPT to help draft survey questions,
                then revised them with teacher feedback." / "Students used
                Python with Copilot for data analysis code." / "No AI tools
                used." / "AI tool used for [specific purpose] — disclosed here."]
   Note: AI use is not prohibited. Transparency is required. A project that
   used AI tools and discloses it is acceptable. A project that used AI tools
   and does not disclose it, and is later found to have done so, is not
   accepted.

Contributor (submitting on behalf of students / institution):
   Name:                     [Teacher / faculty sponsor name, or individual
                           student name if submitting independently]
   Role:                     [Teacher / Faculty / Student / Other]
   Contact:                  [Email / phone]

Date:                       [YYYY-MM-DD]

---
Community Liaison review:
  Acknowledged (within 5 business days):    [Date acknowledged]
  Sponsor confirmed (teacher/faculty):      [Yes / No — name of sponsor who
                           confirmed]
  Student privacy preferences recorded:      [Yes / No — what was recorded]
  AI use disclosed (if applicable):          [Yes / No / N/A]
  Methodology documented for CGB review:     [Yes / No — what's missing]
  Data quality acceptable for intended use:  [Yes / No — explain. Note: not
                           all student data needs to meet professional
                           analyst standards — the bar is whether the
                           contribution is useful and honest for its
                           intended purpose.]
  Could affect a report or indicator:        [Yes / No — which one(s)]
  Tier recommendation:           [Tier 4 (anecdotal/illustrative) /
                           Tier 3 (elevated to expert interview / structured
                           survey) / Tier 2 (elevated to structured survey
                           with good sample — requires Methodologist and
                           Data Steward agreement) / Not ratable]
  Decision:  [NOTED_AND_CREDITED / INVESTIGATING /
              ELEVATED_TO_TIER_3 — for specific use: explain /
              ELEVATED_TO_TIER_2 — for specific use: explain /
              FLAGGED_TO_DATASTEWARD (if data could enter catalog) /
              ROUTED_TO_ANALYSIS_FOR_FURTHER_WORK /
              RETURNED (explain) /
              RESOLVED — explain]
  Date:      [YYYY-MM-DD]
  Reviewer:  [Community Liaison name]
```

---

### E.4: DIRECT_CONTRIBUTION.md (Pathway I — simplified catch-all)

```
DIRECT CITIZENRY CONTRIBUTION
=============================

(This is the simplest possible submission form. If you know what you want
to contribute but aren't sure which pathway to use, use this one. The
Community Liaison will route it to the right place.)

What do you want to contribute?  [Free text — be as specific as you can.
                           What did you see, know, think, or find?]

What's your basis for knowing this?  [Free text — why do you believe this
                           is accurate? Personal experience? Saw it happen?
                           Verified with someone? Have documentation?
                           Heard it from someone you trust?]

What decision or report do you think this relates to?  [Free text — optional.
                           If you're not sure, write "Not sure — please route
                           this where it belongs."]

Anything else you'd like to add?  [Free text — optional. Context, concerns,
                           ideas for what Project Volusia should cover, feedback
                           on the contribution process itself, etc.]

Contact info (optional):       [Name / Email / Phone — only what you're
                           comfortable sharing. You can submit anonymously.]

Date:                           [YYYY-MM-DD]

---
Community Liaison review:
  Acknowledged (within 5 business days):    [Date acknowledged]
  Routed to pathway:                         [A / B / C / D / E / F / G / H
                           / I / NA — explain]
  Action taken:                              [Noted / Investigating /
                           Flagged to Data Steward / Routed to other
                           pathway / Resolved / Other — explain]
  Date:      [YYYY-MM-DD]
  Reviewer:  [Community Liaison name]
```
COMMUNITY INPUT
===============

What I Observed / Know:  [Be specific. "The seafood restaurant at 123
                        Main St, Daytona Beach, closed in March 2026."
                        Not "some restaurants are struggling."]

Where:                    [Address, neighborhood, city, or general area]
When:                     [Date or date range of the observation, or
                        general time period]

Why I Believe It's Accurate:  [e.g., "I visited it regularly and saw it
                        close." / "The owner told me." / "I have a photo
                        of the closure sign." / "This is commonly known
                        among regular customers."]

What Decision or Report This Might Affect:  [e.g., "The Q3 2026 Quarterly
                        Economic Briefing's small business section."
                        / "The tourism attraction performance layer."
                        / "N/A — just flagging for the record."]

Contributor:              [Name (optional) / Neighborhood or role (e.g.,
                        "Daytona Beach resident" / "New Smyrna business
                        owner") / Contact preference (email / phone / no
                        follow-up)]

Date:                     [YYYY-MM-DD]

---
Community Liaison review:
  Acknowledged (within 5 business days):    [Date acknowledged]
  Cross-checked against available sources:   [Yes / No — explain what was
                        checked and what was found]
  Could affect a report or indicator:        [Yes / No — which one(s)]
  Decision:  [NOTED / INVESTIGATING /
              FLAGGED_TO_DATASTEWARD /
              RESOLVED — explain]
  Date:      [YYYY-MM-DD]
  Reviewer:  [Community Liaison name]
```

---

## APPENDIX F: SUMMARY OF CONTRIBUTION PATHWAYS

```
PATHWAY  | WHO                          | WHAT                    | TEMPLATE
---------|------------------------------|-------------------------|----------
A        | Data source discoverer       | New source or update    | A
B        | Analyst / researcher         | Analysis with method    | B
C        | Developer / engineer         | Tool                    | C
D        | GIS pro / cartographer       | Map layer               | D
E        | Writer / editor / SME        | Report content          | (direct)
F        | Resident / business owner /  | Community knowledge     | E
         | community organization /     | (incl. direct           |
         | any citizenry                | contribution catch-all) |
G        | Social media monitor /       | Social media & public   | E.2
         | public footprint contributor  | footprint intelligence  |
H        | K-12 teacher / student /     | Classroom projects,     | E.3
         | college faculty / student /  | faculty research,       |
         | educational institution       | citizen science,        |
         |                              | educational use requests |
I        | Any citizen / visitor /       | Direct catch-all        | E.4
         | investor (unsure of pathway)  | contribution            |
J        | Programmatic contributor /    | API-driven contribution  | J
         | software / bot / agent        | (all pathways via API)  |
I        | Any citizen / visitor /       | Direct catch-all        | E.4
         | investor (unsure of pathway)  | contribution            |
```

**Pathway selection guide:**

   CONTRIBUTOR KNOWS WHAT THEY'RE CONTRIBUTING
   -> Use the pathway that matches:
      - A new data source or update?          -> A
      - An analysis or research project?      -> B
      - A tool or script?                     -> C
      - A map or spatial data?                -> D
      - Report draft or editorial content?    -> E
      - Ground-level knowledge, observation,  -> F
        or personal experience?
      - Social media monitoring or public     -> G
        footprint intelligence?
      - School or college project?            -> H
      - Not sure?                             -> I (Community Liaison routes it)

   CONTRIBUTOR DOESN'T KNOW THE PATHWAY STRUCTURE
   -> Use I (Direct Citizenry Contribution). The Community Liaison
      routes it. No penalty for using the catch-all.

   CONTRIBUTOR IS A PROGRAM (bot, agent, script, software):
   -> Use the Contribution API (Appendix J). Register for an API key,
      use the appropriate submission endpoint (/submissions/{pathway}
      for human-pathway-equivalent submissions, /submissions/agent-item
      for agent ITEMs), follow the API rate limits and auth requirements.
      The API is described in Appendix J.
```

---

---

## APPENDIX J: API CONTRIBUTION ENDPOINTS

The Project Volusia Contribution API is the machine-readable interface for
submitting contributions, checking submission status, retrieving contributor
records, and (for authorized agents) operating within the system. This
appendix defines the endpoints, authentication, rate limits, and the
request/response schemas.

Full OpenAPI 3.0 specification: `CONTRIBUTION/api/openapi.yaml` (or
`https://api.project-volusia.org/openapi.yaml` when the public API is
deployed).

---

### J.1 API Overview

**Base URL:** `https://api.project-volusia.org/api/v1` (production)
            `https://api-staging.project-volusia.org/api/v1` (staging)

**Authentication:** Bearer token in the `Authorization` header:
   `Authorization: Bearer <api_key_or_oauth_token>`

**Content types:**
   - Request: `application/json` (standard), `multipart/form-data` (file
     uploads)
   - Response: `application/json`

**Common response headers:**
   - `X-API-Version: 2026-09-03` — the version of the API that produced
     this response
   - `X-RateLimit-Limit: <N>` — requests allowed per window
   - `X-RateLimit-Remaining: <N>` — requests remaining in current window
   - `X-RateLimit-Reset: <unix_timestamp>` — when the rate limit window
     resets
   - `Retry-After: <seconds>` — included with 429 and 503 responses

**Common error format:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description of the problem",
    "details": [                    // optional — per-field errors for
      { "field": "what_i_know",    //    validation failures
        "message": "specific issue" }
    ],
    "request_id": "req_abc123"     // include this when contacting support
  }
}
```

**HTTP status codes:**
   - 200 — Success
   - 201 — Created (new resource)
   - 202 — Accepted (submission queued for review, not yet decided)
   - 204 — No content (successful deletion, or endpoint with no body)
   - 400 — Bad request (validation error, malformed JSON)
   - 401 — Unauthorized (missing or invalid API key)
   - 403 — Forbidden (valid key, but not authorized for this action)
   - 404 — Not found
   - 409 — Conflict (e.g., duplicate submission ID for idempotent retry)
   - 429 — Too many requests (rate limit exceeded)
   - 500 — Internal server error
   - 503 — Service unavailable (degraded; Retry-After header included)

---

### J.2 Authentication Endpoints

| Method | Path                        | Description                    | Auth required    |
|--------|-----------------------------|--------------------------------|------------------|
| POST   | /auth/register              | Register a new contributor     | None (public)    |
| POST   | /auth/login                 | Exchange credentials for token | None (public)    |
| POST   | /auth/refresh               | Refresh an expiring token      | Valid token      |
| GET    | /auth/me                    | Get current contributor profile| Valid token      |
| POST   | /auth/revoke                | Revoke current token           | Valid token      |

**J.2.1 POST /auth/register**

Registers a new contributor account and returns a pending state. The
contributor completes onboarding by submitting a first contribution or
confirming their email.

Request:
```json
{
  "contributor_type": "individual" | "organization" | "educational_institution" | "agent",
  "contact_email": "contributor@example.com",
  "preferred_name": "Jane Doe",           // or organization name, or agent ID
  "pathway_interest": ["F", "I"],         // which pathways they expect to use
  "agree_to_terms": true                  // must acknowledge the contribution standards
}
```

Response (201 Created):
```json
{
  "contributor_id": "cust_abc123",
  "status": "pending",                     // pending | active | suspended
  "api_key": "pv_abc123...",               // immediate key for tentative use
  "api_key_expires_at": "2026-10-03T00:00:00Z",  // key valid until onboarding completes
  "rate_limit_tier": "public_registered",
  "message": "Account created. Submit your first contribution to complete onboarding."
}
```

**J.2.2 POST /auth/login**

Request:
```json
{
  "contact_email": "contributor@example.com",
  "password": "..."
}
```

Response (200 OK):
```json
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "rt_abc123...",
  "contributor_id": "cust_abc123",
  "rate_limit_tier": "public_registered"
}
```

---

### J.3 Submission Endpoints

All submission endpoints follow the same pattern:

1. **POST /submissions/{pathway}** — submit a new contribution
2. **GET /submissions/{submission_id}** — retrieve a submission and its
   review status
3. **GET /submissions** — list submissions for the authenticated
   contributor (with pagination)

Pathway-specific endpoints:

| Method | Path                        | Pathway    | Auth tier           |
|--------|-----------------------------|------------|---------------------|
| POST   | /submissions/F              | F (Community Knowledge) | public_anonymous, public_registered |
| POST   | /submissions/G              | G (Social Media) | public_registered, trusted_contributor |
| POST   | /submissions/H              | H (Educational Institution) | public_registered, trusted_contributor |
| POST   | /submissions/I              | I (Direct Citizenry) | public_anonymous, public_registered |
| POST   | /submissions/B              | B (Analysis) | trusted_contributor |
| POST   | /submissions/A              | A (Data Source) | trusted_contributor |
| POST   | /submissions/C              | C (Tool) | trusted_contributor |
| POST   | /submissions/D              | D (Map Layer) | trusted_contributor |
| POST   | /submissions/E              | E (Report Content) | trusted_contributor |

**J.3.1 POST /submissions/F — Community Knowledge Submission (Pathway F)**

This is the API equivalent of the COMMUNITY_INPUT.md template (Appendix E.1).

Request body (mirrors the template fields):
```json
{
  "what_i_know": "The seafood restaurant at 123 Main St, Daytona Beach, closed in March 2026.",
  "where": "123 Main St, Daytona Beach",
  "when": "2026-03-15",
  "why_believe_accurate": "I visited it regularly and saw it close. The owner told me.",
  "what_decision_or_report": "The Q3 2026 Quarterly Economic Briefing's small business section.",
  "channel_used": "web_form",               // web_form | email | sms | phone | library | meeting_card | social_media | other
  "contributor_display": "Daytona Beach resident",  // what to show if credited
  "contact_preference": "email",            // email | phone | no_follow_up
  "contact_email": "contributor@example.com",  // only if contact_preference != no_follow_up
  "idempotency_key": "idem_abc123"          // optional — for safe retry
}
```

Response (201 Created):
```json
{
  "submission_id": "sub_fgh789",
  "pathway": "F",
  "status": "queued",                       // queued | under_review | accepted | returned | rejected | resolved | noted
  "submitted_at": "2026-09-03T14:22:00Z",
  "acknowledged_at": "2026-09-04T09:00:00Z",   // when Community Liaison acknowledged
  "estimated_review_by": "2026-09-08T23:59:59Z",  // 5 business days from acknowledgment
  "message": "Submission received. You will receive an update within 5 business days.",
  "idempotency_key": "idem_abc123"           // echoed back if provided
}
```

Idempotency: if the same `idempotency_key` is used for a second request
within 24 hours, the server returns the original response (200 OK) instead
of creating a duplicate submission.

**J.3.2 POST /submissions/I — Direct Citizenry Contribution (Pathway I)**

The simplest API endpoint. Mirrors the DIRECT_CONTRIBUTION.md template
(Appendix E.4).

Request body:
```json
{
  "what_to_contribute": "I think the quarterly report should cover the impact of short-term rentals on long-term housing availability in Daytona Beach. I've seen three families move out of my neighborhood in the past year because their landlords converted their apartments to STRs.",
  "basis": "I live in the neighborhood (Deltona Park, Daytona Beach). I know the families personally. Two of them gave me written statements.",
  "what_decision_or_report": "Not sure — annual report? housing section?",
  "anything_else": "I'd be willing to talk to someone if that would help.",
  "contact_preference": "email",
  "contact_email": "contributor@example.com",
  "idempotency_key": "idem_xyz789"
}
```

Response: same structure as J.3.1.

**J.3.3 POST /submissions/G — Social Media / Public Footprint Submission (Pathway G)**

Mirrors the SOCIAL_MEDIA_INPUT.md template (Appendix E.2). This is a
larger request — it includes the full methodology documentation.

Request body:
```json
{
  "contribution_type": "social_media_intelligence",  // | crowdsourced_intelligence | public_platform_data
  "platforms_monitored": ["twitter", "reddit"],
  "query_keywords": ["Volusia water quality", "#OrmondBeach"],
  "time_period_covered": {"start": "2026-08-01", "end": "2026-08-15"},
  "language": "en",
  "geographic_filter": "posts_mentioning_volusia",
  "summary_of_signal": "Over 2 weeks, mentions of 'water quality' at Ormond Beach increased 3x vs prior 2-week baseline. Majority of posts expressed concern. No official advisory issued as of Aug 15.",
  "volume": "~40 posts across Twitter and Reddit over 14 days",
  "sentiment_direction": "negative",
  "themes_identified": ["Water quality concern", "Praise for beach cleanup", "Questions about county testing"],
  "representative_quotes": [
    {"platform": "twitter", "date": "2026-08-10", "quote": "[paraphrased] 'Has anyone else noticed the water looks brown at Ormond Beach this week?'}", "attribution": "anonymous"}
  ],
  "platform_data": null,  // if contributing public platform data instead, include here
  "methodology_collection": "Searched Twitter and Reddit daily for keywords. Captured all public posts from accounts self-identifying as Volusia residents or visitors. Deduplicated by content. Aggregated by day.",
  "methodology_excluded": "Private accounts, deleted posts, spam, non-English posts (unless monitor can assess).",
  "methodology_limitations": "Twitter users are not representative of Volusia population — younger, more urban, more likely tourists. Signal shows sentiment among Twitter users who mention Volusia, not all residents.",
  "methodology_platform_demographics": "Twitter skews 18-49, urban. Reddit skews 18-35, urban. Neither is a probability sample.",
  "confidence_level": "directional_only_tier4",
  "possible_investigation": "Check NOAA / county water quality data for recent readings at Ormond Beach. Check weather events.",
  "possible_report_use": "Monthly Tourism Update — emerging issue watch.",
  "contributor_display": "Community Monitor",
  "contact_preference": "email",
  "contact_email": "monitor@example.com",
  "idempotency_key": "idem_g123"
}
```

Response: same structure as J.3.1.

**J.3.4 POST /submissions/H — School Project Submission (Pathway H)**

Mirrors the SCHOOL_PROJECT_SUBMISSION.md template (Appendix E.3). This is
the largest submission endpoint — it includes student privacy, AI use
disclosure, and methodology for CGB review.

Request body is the full template from Appendix E.3. Response is the same
as J.3.1, with the addition of a `tier_recommendation` field in the
acknowledgment if the Community Liaison has already done a preliminary
review.

---

### J.4 Status and Review Endpoints

**GET /submissions/{submission_id}**

Retrieve a submission and its current status. Includes the review history
if the submission has been reviewed.

Response:
```json
{
  "submission_id": "sub_fgh789",
  "pathway": "F",
  "status": "accepted",
  "submitted_at": "2026-09-03T14:22:00Z",
  "acknowledged_at": "2026-09-04T09:00:00Z",
  "reviewed_at": "2026-09-06T11:30:00Z",
  "decision": "accepted",
  "decision_details": "Added to community knowledge base. May be cited as context in the Q4 2026 Economic Briefing if verified.",
  "reviewer": "Community Liaison (name)",
  "contributor_display": "Daytona Beach resident",
  "credit_option": "credited",             // credited | anonymous | school_only | not_credited
  "publication_note": null,                // if accepted for publication, what was published
  "next_steps": null
}
```

**GET /submissions**

List submissions for the authenticated contributor. Paginated.

Query parameters:
   - `page` (default 1)
   - `per_page` (default 20, max 100)
   - `status` (optional filter: queued, under_review, accepted, returned, rejected, resolved, noted)

Response:
```json
{
  "data": [
    {
      "submission_id": "sub_fgh789",
      "pathway": "F",
      "status": "accepted",
      "submitted_at": "2026-09-03T14:22:00Z",
      "decision": "accepted"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 3,
    "total_pages": 1
  }
}
```

---

### J.5 Agent ITEM Submission Endpoint

**POST /submissions/agent-item**

The endpoint for AI agents (Tier 1, 2, and 3) to submit structured ITEMs
to the system. This is the programmatic interface for the agent ITEM format
defined in Appendix G. Agents use this instead of the pathway-specific
endpoints — a single endpoint for all agent-generated submissions.

Auth required: `agent_verified` tier or higher.

Request body (maps to the ITEM schema):
```json
{
  "itemtype": "monitoring_event",       // monitoring_event | processing_result | synthesis_draft | quality_flag | cross_reference | submission_item
  "agent_id": "census_monitor_v1",
  "agent_version": "1.2.0",
  "timestamp": "2026-09-03T14:22:00Z",
  "source": "ACS_2023_5YR_B19013",        // data source or tool this relates to
  "confidence": 0.92,                      // agent self-assessed confidence
  "content": {
    "source": "ACS_2023_5YR_B19013",
    "change_type": "new_vintage",
    "detail": "New ACS 2023 5-year vintage released. Previous vintage: 2022. Tables affected: B19013, B19001, B17001.",
    "timestamp": "2026-09-03T14:22:00Z"
  },
  "flags": ["new_vintage", "review_needed"],
  "next_action": "human_review_required",
  "human_owner": "Data Steward",
  "idempotency_key": "idem_agent_20260903_1422"
}
```

Response (202 Accepted):
```json
{
  "submission_id": "sub_agent_456",
  "status": "queued",
  "routed_to": "Data Steward",
  "estimated_review_by": "2026-09-05T23:59:59Z",
  "message": "Agent ITEM received and routed to Data Steward queue.",
  "idempotency_key": "idem_agent_20260903_1422"
}
```

Agent ITEM validation rules:
   - `itemtype` must be one of the six allowed values
   - `agent_id` must match a registered agent (checked against agent_records)
   - `human_owner` must be a valid CGB member
   - `flags` must be a subset of the allowed flags
   - `next_action` must be one of the allowed values
   - `confidence` must be between 0.0 and 1.0
   - If `itemtype` is `synthesis_draft`, the request MUST include a
     `sources_cited` field in `content` listing every source used
   - If `content` contains a claim about Volusia, the request MUST include
     a `sources_cited` field (the agent cannot make unverifiable claims)

---

### J.6 Data Access Endpoints (for authorized contributors)

These endpoints let trusted contributors (educational institution partners,
standing contributors doing research) access Project Volusia data for
classroom or research use. They do NOT let anyone publish — they are
consumption endpoints.

| Method | Path                        | Description                    | Auth tier           |
|--------|-----------------------------|--------------------------------|---------------------|
| GET    | /data/sources               | List registered data sources   | trusted_contributor |
| GET    | /data/sources/{source_id}   | Get details on one source      | trusted_contributor |
| GET    | /data/tables                | List cataloged tables          | trusted_contributor |
| GET    | /data/tables/{table_id}     | Get table schema + metadata    | trusted_contributor |
| GET    | /data/tables/{table_id}/samples | Get sample rows (not full dataset) | trusted_contributor |
| GET    | /data/metadata              | Get data catalog metadata index| trusted_contributor |
| GET    | /reports/{report_id}        | Get a published report         | public_registered, trusted_contributor |
| GET    | /reports/upcoming           | Get schedule of upcoming reports | public_registered, trusted_contributor |
| GET    | /tools                      | List registered tools          | trusted_contributor |

These are read-only endpoints. They do not allow modification of the
knowledge base. Full data access (downloading entire datasets) is handled
via direct file access or the data portal, not through the contribution API.

---

### J.7 Contributor Record Endpoints

**GET /contributors/me/record**

Retrieve the authenticated contributor's CONTRIBUTION_RECORD (mirrors the
record described in Section 2.2).

Response:
```json
{
  "contributor_id": "cust_abc123",
  "standing": "active",                    // pending | active | suspended
  "pathways_used": ["F", "I"],
  "total_submissions": 12,
  "accepted": 9,
  "returned": 2,
  "rejected": 1,
  "acceptance_rate": 0.75,
  "median_time_to_review_days": 3.5,
  "quality_score_avg": 4.2,                // average quality score of accepted submissions
  "repeatability": "consistent",           // consistent | bursty | infrequent
  "credit_option": "credited",
  "last_activity": "2026-09-03T14:22:00Z",
  "since": "2026-06-01T00:00:00Z"         // record starts here
}
```

---

### J.8 Rate Limits

Rate limits are per API key, per endpoint category.

| Tier                | Submission endpoints | Data access endpoints | File uploads | Burst allowance |
|---------------------|----------------------|-----------------------|--------------|-----------------|
| public_anonymous   | 5 / hour             | none                  | none         | 2 in 10s        |
| public_registered   | 20 / hour            | none                  | 2 / hour     | 5 in 10s        |
| trusted_contributor | 60 / hour            | 120 / hour            | 10 / hour    | 15 in 10s       |
| agent_verified      | configurable         | configurable          | configurable | configurable    |
| cgb_member          | configurable         | configurable          | configurable | configurable    |
| system_internal     | no limit             | no limit              | no limit     | no limit        |

When a rate limit is exceeded, the response is:
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Retry after 2026-09-03T15:00:00Z.",
    "retry_after": "2026-09-03T15:00:00Z"
  }
}
```
HTTP status: 429.

Rate limits can be increased for individual contributors on request to the
Community Liaison (for human contributors) or the Agent Operations Lead (for
agents). Increases are logged in the contributor record.

---

### J.9 API Versioning and Deprecation

The API version is part of the URL path: `/api/v1/`, `/api/v2/`, etc.
Within a major version, additive changes (new endpoints, new optional
fields) are non-breaking and do not require a version bump. Breaking
changes (removing endpoints, removing required fields, changing field
types) require a new major version.

When a new major version is released:
   - The old version continues to serve for at least 90 days.
   - Responses from the old version include a `Sunset` header with the
     shutdown date.
   - The old version's documentation is archived at
     `/docs/api/v1/deprecated.html` (or equivalent).
   - Contributors with API keys registered on the old version receive
     email notification of the deprecation 30 days, 14 days, and 7 days
     before shutdown.

Example deprecation header:
```
Sunset: Sat, 01 Nov 2026 00:00:00 GMT
Link: </api/v2/submissions/F>; rel="successor-version"
```

---

### J.10 Error Handling and Retry Guidance

**Transient errors (retry):**
   - 429 Rate Limit Exceeded — wait for Retry-After, then retry.
   - 503 Service Unavailable — wait for Retry-After, then retry.
   - 502/504 Network errors — exponential backoff (1s, 2s, 4s, 8s, max
     30s), max 3 retries.

**Non-transient errors (do not retry):**
   - 400 Bad Request — fix the request before retrying.
   - 401 Unauthorized — check the API key.
   - 403 Forbidden — the key is not authorized for this action.
   - 404 Not Found — the resource does not exist.
   - 409 Conflict — for idempotent submissions, this means the submission
     was already processed; retrieve it via GET /submissions/{id}.

**Idempotent submission pattern:**
   1. Generate an idempotency_key (UUID recommended) before making the
      request.
   2. Submit with the idempotency_key in the request body.
   3. If you get a network error or 5xx, retry with the SAME
      idempotency_key.
   4. If the retry returns 200 with an existing submission_id, you're
      done — the submission was created on the first attempt.
   5. If the retry returns 201 with a new submission_id, something went
      wrong (the first request's response was lost but the submission may
      or may not have been created). Check GET /submissions/{submission_id}
      for both IDs. If both exist, keep the earlier one and flag the
      duplicate for the Community Liaison to merge or reject.

---

### J.11 Example: Submitting a Community Knowledge Contribution via curl

```bash
curl -X POST https://api.project-volusia.org/api/v1/submissions/F \
  -H "Authorization: Bearer pv_abc123..." \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: idem_abc123" \
  -d '{
    "what_i_know": "The seafood restaurant at 123 Main St, Daytona Beach, closed in March 2026.",
    "where": "123 Main St, Daytona Beach",
    "when": "2026-03-15",
    "why_believe_accurate": "I visited it regularly and saw it close.",
    "what_decision_or_report": "Q3 2026 Quarterly Economic Briefing small business section",
    "channel_used": "web_form",
    "contributor_display": "Daytona Beach resident",
    "contact_preference": "email",
    "contact_email": "contributor@example.com"
  }'
```

Response (201 Created):
```json
{
  "submission_id": "sub_fgh789",
  "pathway": "F",
  "status": "queued",
  "submitted_at": "2026-09-03T14:22:00Z",
  "message": "Submission received. You will receive an update within 5 business days."
}
```

---

### J.12 Example: Agent Submitting a Monitoring Event via Python

```python
import requests
import uuid

API_BASE = "https://api.project-volusia.org/api/v1"
API_KEY = "pv_agent_..."  # issued to the agent's owner

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

item = {
    "itemtype": "monitoring_event",
    "agent_id": "census_monitor_v1",
    "agent_version": "1.2.0",
    "timestamp": "2026-09-03T14:22:00Z",
    "source": "ACS_2023_5YR_B19013",
    "confidence": 0.92,
    "content": {
        "source": "ACS_2023_5YR_B19013",
        "change_type": "new_vintage",
        "detail": "New ACS 2023 5-year vintage released.",
        "timestamp": "2026-09-03T14:22:00Z"
    },
    "flags": ["new_vintage", "review_needed"],
    "next_action": "human_review_required",
    "human_owner": "Data Steward",
    "idempotency_key": str(uuid.uuid4())
}

response = requests.post(
    f"{API_BASE}/submissions/agent-item",
    headers=headers,
    json=item,
    timeout=10
)

if response.status_code == 202:
    submission = response.json()
    print(f"Submission {submission['submission_id']} queued. Routed to: {submission['routed_to']}")
elif response.status_code == 429:
    retry_after = response.json().get("retry_after")
    print(f"Rate limited. Retry after: {retry_after}")
elif response.status_code >= 500:
    print(f"Server error {response.status_code}. Retry later.")
else:
    print(f"Error {response.status_code}: {response.json()['error']['message']}")
```

---

### J.13 API Health Endpoint

**GET /health**

Returns the health of the contribution API. Does not require authentication.

Response:
```json
{
  "status": "healthy",                    // healthy | degraded | down
  "version": "2026-09-03",
  "uptime_seconds": 1234567,
  "dependencies": {
    "database": "healthy",
    "submission_queue": "healthy",
    "auth_service": "healthy"
  },
  "rate_limits": {
    "public_anonymous_submissions_remaining": 3,
    "public_anonymous_submissions_reset_at": "2026-09-03T15:00:00Z"
  }
}
```

Monitored by the health check agent (TOOLS_CATALOG.md — health_check tool).

---

### J.14 API Contribution Architecture Diagram (textual)

```
                    ┌─────────────────────────────────────────┐
                    │         CONTRIBUTION API (api.project     │
                    │         -volusia.org/api/v1)              │
                    └──────────┬──────────────────┬────────────┘
                               │                  │
          ┌────────────────────┼──────────────────┼────────────────────┐
          │                    │                  │                    │
   PUBLIC       TRUSTED          AGENT             CGB MEMBER        SYSTEM
   ANONYMOUS    CONTRIBUTOR      VERIFIED          (admin)          INTERNAL
   (rate-limited│ (standing,      (agent swarm,    (full read,      (internal
    submissions,│  educational)    scoped perms)    approve/reject,   services only)
    Pathway F/I)│                (ITEMs,          adjust access     (portal backend,
                │                data access)      revoke keys)       health check,
                │                                  revoke keys)       backup sync)
                │                    │                  │                    │
                ▼                    ▼                  ▼                    ▼
          ┌──────────────────────────────────────────────────────────────┐
          │                    SUBMISSION QUEUE                            │
          │  (queued → under_review → accepted/rejected/returned)        │
          └─────────────────────────┬────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
               COMMUNITY        CGB REVIEW        AGENT REVIEW
               LIAISON          (per pathway       (agent ITEMs
               (manual +        owner)            routed to owner)
               API-accessible)  │
                    │            ▼
                    │     ┌──────────────────────────────────┐
                    │     │  CONTRIBUTION_LOG.md             │
                    │     │  (all decisions, all items)       │
                    │     └──────────────────────────────────┘
                    │            │
                    ▼            ▼
          ┌──────────────────────────────────────────────────────────────┐
          │                  KNOWLEDGE BASE                               │
          │  CONTRIBUTION/submissions/  → submitted items               │
          │  CONTRIBUTION/reviews/      → review decisions              │
          │  CONTRIBUTION/contributor_ → per-contributor records         │
          │    records/                  →                                  │
          │  CONTRIBUTION/agent_records/ → per-agent health records       │
          │  CONTRIBUTION/corrections/  → corrections & retractions      │
          │  CONTRIBUTION/rejected/     → archived rejected items        │
          │                                                                      │
          │  DATA/raw/            → raw downloaded data                      │
          │  DATA/processed/      → cleaned/aggregated                      │
          │  DATA/published/      → ready for reports                        │
          │  REPORTS/working/     → drafts in progress                      │
          │  MAPS/layers/         → geospatial layers                        │
          │  TOOLS/tools/         → tool code                                │
          └──────────────────────────────────────────────────────────────┘
```

---

### J.15 API-First vs. Human-First

The API is an enabler, not a replacement for human contribution. The
design principles:

   1. **Humans first, machines second.** The contribution pathways and
      standards (Sections 2-6, Appendices A-I) define what a valid
      contribution is. The API is the machine interface to those same
      pathways. An API submission is subject to the same review,
      standards, and lifecycle as a human submission.

   2. **The API does not lower the bar.** An API submission that doesn't
      meet the standards for its pathway is rejected or returned with
      feedback, same as a human submission. The API makes submission
      easier, not submission sloppier.

   3. **The API does not raise the bar for humans.** Humans should not
      need an API key to contribute. The manual channels (email, SMS,
      phone, library drop-box, community meeting cards, web form) remain
      available and are first-class contribution pathways.

   4. **Agents submit structured ITEMs, not freeform text.** The
      /submissions/agent-item endpoint requires agents to use the ITEM
      format (Appendix G). This ensures agent contributions are
      machine-parseable, reviewable, and traceable.

   5. **The API makes the system more accessible, not less.** A teacher
      with a class of 30 students should be able to submit their students'
      project via a simple API call (or a web form that calls the API
      behind the scenes), not by learning a complex system. A resident
      who wants to submit a correction should be able to do it in a few
      seconds via SMS or web form. The API supports these interfaces, not
      replaces them.

   6. **API access is a privilege, not a right.** API keys are issued by
      the Community Liaison (for human contributors) or the Agent
      Operations Lead (for agents). Keys can be revoked if abused. Public
      anonymous access is limited to the lowest-tier endpoints. Higher-
      tier access requires registration and trustee status.

---

END OF APPENDIX J

---

## APPENDIX G: AGENT ITEM FORMAT REFERENCE

```
AGENT ITEM SCHEMA
=================

itemtype:  One of:
  - monitoring_event    (source changed, new vintage, broken link)
  - processing_result   (new processed dataset ready)
  - synthesis_draft     (draft section for a report)
  - quality_flag        (anomaly detected, data quality issue)
  - cross_reference     (new source cross-referenced against existing tables)
  - submission_item     (agent-generated submission for human review)

agent_id:  e.g., census_monitor_v1, acs_processor_v1, briefing_synth_v1

timestamp:  ISO 8601, e.g., 2026-09-03T14:22:00Z

source:  Which data source / tool / method this relates to (by ID or name)

confidence:  0.0-1.0, the agent's self-assessed confidence in its output.
  NOT a claim of correctness — it's "how sure is the agent that this
  output is what it thinks it is" (not "how sure is the agent that
  this is true about Volusia").

content:  The actual payload (structured, not freeform):
  - For monitoring_event: {source, change_type, detail, timestamp}
  - For processing_result: {input_vintage, pipeline_version, output_files,
    row_counts, flagged_issues}
  - For synthesis_draft: {section, draft_text, sources_cited,
    uncertainty_statements, flags}
  - For quality_flag: {source, issue_type, detail, suggested_action}
  - For cross_reference: {new_source, related_tables, join_keys,
    methodology_differences, notes}
  - For submission_item: {item_type, content_per_APPENDIX_A-I,
    reviewer_recommendation}

flags:  List of flags:
  - new_vintage
  - format_changed
  - missing_values
  - out_of_range
  - review_needed
  - auto_accept_candidate
  - emergency_relevant

next_action:  One of:
  - human_review_required
  - auto_accept         (for low-risk, high-confidence items that still
                        log but don't require human action)
  - agent_followup      (the agent will check again later)

human_owner:  Which CGB member owns this item (for routing):
  - Data Steward
  - Methodologist
  - Tool Owner
  - GIS Lead
  - Report Lead
  - Community Liaison
```

---

END OF DOCUMENT
