"""Project Volusia - Gamification Engine (weaponized). Persistent JSON state, XP/levels, missions."""
import json
from pathlib import Path
from datetime import datetime
from enum import Enum
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/gamification", tags=["gamification"])
PROJECT_ROOT = Path(__file__).parent.parent.parent
GAMIFICATION_DIR = PROJECT_ROOT / "data" / "gamification"
GAMIFICATION_DIR.mkdir(parents=True, exist_ok=True)
XP_LEVELS = [(0,"Newcomer"),(100,"Explorer"),(500,"Analyst"),(1500,"Steward"),(5000,"Architect")]
MISSION_CATALOG = [
    # Tier 1 — Entry (0–50 XP)
    {"id":"first_spark","name":"First Spark","desc":"Submit your first contribution","xp":50},
    {"id":"explorer_visit","name":"Explorer Visit","desc":"Visit all 7 portal pages","xp":30},
    # Tier 2 — Consistency (100–250 XP)
    {"id":"streak_7","name":"Streak 7","desc":"7-day contribution streak","xp":100},
    {"id":"streak_30","name":"Streak 30","desc":"30-day contribution streak","xp":250},
        {"id":"community_voice","name":"Community Voice","desc":"10+ total contributions","xp":150},
        # Tier 3 — Quality (200–500 XP)
        {"id":"verified","name":"Verified Contributor","desc":"Reach Verified quality tier","xp":200},
        {"id":"data_steward","name":"Data Steward","desc":"5+ accepted submissions","xp":300},
        {"id":"data_architect","name":"Data Architect","desc":"Add a new data source to the pipeline","xp":400},
        {"id":"sector_pioneer","name":"Sector Pioneer","desc":"Submit in all 4 constituencies","xp":400},
    # Tier 3.5 — Knowledge & Findings
    {"id":"knowledge_seeker","name":"Knowledge Seeker","desc":"Submit 5+ knowledge contributions","xp":250},
    {"id":"finding_master","name":"Finding Master","desc":"Submit 10+ findings","xp":350},
    {"id":"resource_curator","name":"Resource Curator","desc":"Submit 5+ resources/tools","xp":300},
    {"id":"data_contributor","name":"Data Contributor","desc":"Submit 10+ data points","xp":300},
    {"id":"cross_validator","name":"Cross-Validator","desc":"Verify 5+ contributions from others","xp":400},
    # Tier 4 — Impact (500–2000 XP)
    {"id":"analyst","name":"Analyst","desc":"Reach Analyst level (500 XP)","xp":0},
    {"id":"researcher","name":"Researcher","desc":"Submit 3+ stakeholder interviews","xp":500},
    {"id":"governor","name":"Governor","desc":"Contribute to governance docs","xp":350},
    {"id":"community_builder","name":"Community Builder","desc":"20+ total contributions","xp":600},
    {"id":"source_master","name":"Source Master","desc":"Contribute to 5+ data sources","xp":450},
    {"id":"quality_guardian","name":"Quality Guardian","desc":"Verify 10+ submissions","xp":300},
    {"id":"mentor","name":"Mentor","desc":"Help a new contributor submit","xp":250},
    {"id":"business_expert","name":"Business Expert","desc":"3+ business pathway contributions","xp":350},
    {"id":"community_champion","name":"Community Champion","desc":"5+ resident pathway contributions","xp":350},
    {"id":"visitor_insights","name":"Visitor Insights","desc":"3+ tourist pathway contributions","xp":350},
    {"id":"industry_leader","name":"Industry Leader","desc":"2+ industry mover pathway contributions","xp":400},
    {"id":"multi_constituency","name":"Multi-Constituency","desc":"10+ contributions across all pathways","xp":500},
    # Tier 4.5 — Infrastructure & Code Contributors
    {"id":"code_committer","name":"Code Commiter","desc":"Submit a PR that passes CI","xp":300},
    {"id":"infrastructure_builder","name":"Infrastructure Builder","desc":"Fix or improve deployment/infra","xp":400},
    {"id":"ci_cd_contributor","name":"CI/CD Contributor","desc":"Improve or add CI/CD pipeline","xp":450},
    {"id":"test_contributor","name":"Test Contributor","desc":"Add tests covering new code","xp":350},
    {"id":"doc_contributor","name":"Documentation Contributor","desc":"Improve docs, guides, or examples","xp":250},
    {"id":"review_contributor","name":"Review Contributor","desc":"Review 5+ PRs from others","xp":300},
    # Tier 5 — Legacy (5000+ XP)
    {"id":"architect","name":"Architect","desc":"Reach Architect level (5000 XP)","xp":0},
    {"id":"visionary","name":"Visionary","desc":"Reach 10,000 total XP","xp":0},
    {"id":"legacy_builder","name":"Legacy Builder","desc":"Contribute to all 11 data categories","xp":1000},
        # Tier 6 — Civic & Community Engagement
        {"id":"civic_participant","name":"Civic Participant","desc":"Attend 1+ public meeting or hearing","xp":100},
        {"id":"data_citizen","name":"Data Citizen","desc":"Verify 5+ data points against primary sources","xp":150},
        {"id":"open_intelligence_advocate","name":"Open Intelligence Advocate","desc":"Share Project Volusia with 10+ people","xp":200},
        {"id":"transparency_champion","name":"Transparency Champion","desc":"Request FOIA or public records 3+ times","xp":300},
        {"id":"policy_contributor","name":"Policy Contributor","desc":"Submit data-backed policy recommendations","xp":400},
        {"id":"budget_analyst","name":"Budget Analyst","desc":"Analyze 3+ budget documents and share findings","xp":350},
        {"id":"census_participant","name":"Census Participant","desc":"Complete 2030 Census or ACS survey","xp":150},
        {"id":"community_organizer","name":"Community Organizer","desc":"Coordinate 3+ community data drives","xp":450},
        {"id":"youth_mentor","name":"Youth Mentor","desc":"Mentor a student on a school project (Pathway G)","xp":250},
        {"id":"senior_advisor","name":"Senior Advisor","desc":"Submit observations as a Pathway K contributor","xp":200},
        # Tier 7 — Environmental & Public Health Stewardship
        {"id":"environmental_steward","name":"Environmental Steward","desc":"Report 5+ environmental observations (Pathway Q)","xp":300},
        {"id":"climate_analyst","name":"Climate Analyst","desc":"Submit 3+ climate/weather observations","xp":250},
        {"id":"public_health_advocate","name":"Public Health Advocate","desc":"Contribute health access data (Pathway M)","xp":350},
        {"id":"safety_reporter","name":"Safety Reporter","desc":"Report 5+ safety/hazard observations (Pathway P)","xp":300},
        {"id":"agriculture_steward","name":"Agriculture Steward","desc":"Contribute farming/maritime data (Pathway N)","xp":300},
        {"id":"water_quality_monitor","name":"Water Quality Monitor","desc":"Submit 3+ water quality observations","xp":250},
        # Tier 8 — Research & Data Science
        {"id":"data_scientist","name":"Data Scientist","desc":"Build a visualization or analysis tool","xp":450},
        {"id":"statistical_modeler","name":"Statistical Modeler","desc":"Create predictive model for Volusia data","xp":500},
        {"id":"geospatial_analyst","name":"Geospatial Analyst","desc":"Add GeoJSON map layer with analysis","xp":400},
        {"id":"corpus_builder","name":"Corpus Builder","desc":"Compile 100+ structured data points","xp":350},
        {"id":"open_data_curator","name":"Open Data Curator","desc":"Curate and publish a public dataset","xp":450},
        {"id":"api_developer","name":"API Developer","desc":"Build a public API integration for Volusia data","xp":400},
        # Tier 9 — Governance & Institutional Impact
        {"id":"board_advisor","name":"Board Advisor","desc":"Present findings to county board or commission","xp":500},
        {"id":"grant_writer","name":"Grant Writer","desc":"Use Volusia data to secure 1+ grant","xp":450},
        {"id":"institutional_partner","name":"Institutional Partner","desc":"Partner with a government/NGO institution","xp":400},
        {"id":"policy_influencer","name":"Policy Influencer","desc":"Data cited in 1+ official policy document","xp":500},
        # Tier 10 — Legend
        {"id":"legend","name":"Legend","desc":"Reach 50,000 total XP","xp":0},
        {"id":"founder","name":"Founder","desc":"Founding contributor since launch","xp":0},
    ]
class SubmissionType(str, Enum):
    KNOWLEDGE = "knowledge"
    FINDINGS = "findings"
    RESOURCE = "resource"
    DATA = "data"
    INDICATOR = "indicator"

class QualityTier(str, Enum):
    VERIFIED="verified"; REVIEWED="reviewed"; PENDING="pending"; FLAGGED="flagged"
class ContributeRequest(BaseModel):
    contributor_id: str
    pathway: str = Field(..., pattern=r"^[A-Na-n]$|^agent-item$")
    submission_type: str = Field(default="knowledge", description="Type: knowledge, findings, resource, data, indicator")
    submission: dict = Field(default_factory=dict)
    source: str = Field(..., description="Source URL or identifier")
    verified: bool = Field(default=False, description="Whether contribution is verified")
    tags: list = Field(default_factory=list, description="Tags for categorization")
_gam_state: dict = {}
_contributions: list = []
def _now_iso(): return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
def _level_for_xp(xp):
    l="Newcomer"
    for t,n in XP_LEVELS:
        if xp>=t: l=n
    return l
def _quality_score(submission, existing):
    source=submission.get("source",""); vintage=submission.get("vintage","")
    fetched_at=submission.get("fetchedAt",vintage)
    amap={"US Census Bureau":100,"US Census ACS":100,"Census ACS 5-Year":100,"BLS Local Area Unemployment Statistics":100,"BLS LAUS":100,"BLS":100,"NOAA":100,"NOAA NCEI":100,"BEA":100,"Open-Meteo":90,"FCC":95,"Volusia County Property Appraiser":90,"FL DBPR":90,"Zillow":80,"Redfin":80,"Volusia County Convention & Visitors Bureau":90,"Volusia County Building Dept":90,"Volusia Business":85}
    authority=60
    for k,v in amap.items():
        if k.lower() in source.lower(): authority=v; break
    try:
        ft=datetime.fromisoformat(fetched_at.replace("Z","+00:00"))
        age_days=(datetime.utcnow()-ft).total_seconds()/86400.0
    except Exception: age_days=30
    if age_days<=90: vf=100
    elif age_days<=180: vf=60
    elif age_days<=270: vf=30
    elif age_days<=365: vf=10
    else: vf=0
    required=["source","sourceUrl","vintage"]
    mc=sum(1 for k in required if submission.get(k))
    mc=int((mc/len(required))*100)
    desc=submission.get("description","")
    if desc and len(desc)>30: mc=min(100,mc+10)
    value=submission.get("value"); cr=50
    if isinstance(value,(int,float)):
        for ind in existing:
            iname=str(ind.get("name","")).lower(); sname=str(submission.get("name","")).lower()
            if sname in iname or iname in sname:
                iv=ind.get("value")
                if isinstance(iv,(int,float)) and iv!=0:
                    diff=abs(float(value)-float(iv))/abs(float(iv))
                    if diff<0.05: cr=100
                    elif diff<0.15: cr=75
                    elif diff<0.30: cr=50
                    else: cr=25
                    break
    overall=round(authority*0.30+vf*0.25+mc*0.20+cr*0.25,1)
    if overall>=85: tier=QualityTier.VERIFIED.value
    elif overall>=70: tier=QualityTier.REVIEWED.value
    elif overall>=50: tier=QualityTier.PENDING.value
    else: tier=QualityTier.FLAGGED.value
    return {"source_authority":authority,"vintage_freshness":vf,"metadata_completeness":mc,"cross_reference_agreement":cr,"overall":overall,"tier":tier}
def _badge_for_state(state):
    tier=state.get("quality_tier","pending"); streak=state.get("streak",0); acc=state.get("accuracy_rate",0.0); overall=state.get("quality_score",{}).get("overall",0)
    if tier=="verified" and acc>=0.95: return "Platinum Contributor"
    if tier=="verified" and streak>=6: return "Gold Streak"
    if acc>=0.90: return "Silver Accuracy"
    if tier=="reviewed" and streak>=3: return "Bronze Verified"
    if overall>=85 and streak>=7: return "Sector Pioneer"
    return None
def _load_state(cid):
    if cid not in _gam_state:
        fpath=GAMIFICATION_DIR/f"{cid}.json"
        if fpath.exists():
            try: _gam_state[cid]=json.loads(fpath.read_text())
            except Exception: pass
    return _gam_state.setdefault(cid,{"total_xp":0,"level":"Newcomer","streak":0,"best_streak":0,"quality_tier":QualityTier.PENDING.value,"quality_score":{},"badges":[],"joined_date":_now_iso(),"last_contribution_date":_now_iso(),"last_seen_values":{},"review_velocity_days":3.0,"mission_flags":{},"new_sources_added":0,"interviews_completed":0,"gov_contributions":0,"verifications":0,"mentees_helped":0,"pages_visited":[],"sources_contributed":[],"categories_contributed":[],"pathway_counts":{},"prs_merged":0,"infra_fixes":0,"ci_improvements":0,"tests_added":0,"docs_improved":0,"prs_reviewed":0})
def _save_state(cid): (GAMIFICATION_DIR/f"{cid}.json").write_text(json.dumps(_gam_state[cid],indent=2,default=str))
def _save_leaderboard_snapshot(entries):
    week=datetime.utcnow().strftime("%Y-W%U"); (GAMIFICATION_DIR/f"leaderboard-{week}.json").write_text(json.dumps(entries,indent=2,default=str))
@router.post("/contribute",status_code=201)
def contribute(req: ContributeRequest):
    cid=req.contributor_id; state=_load_state(cid); existing=[]; qs=_quality_score(req.submission,existing)
    if req.quality_score: qs=req.quality_score
    now=datetime.utcnow(); last_date_str=state.get("last_contribution_date","")
    try: last_date=datetime.fromisoformat(last_date_str.replace("Z","+00:00")).date()
    except Exception: last_date=None
    today=now.date()
    if last_date and last_date==today: state["streak"]=max(state.get("streak",0),1)
    elif last_date and (today-last_date).days==1: state["streak"]=state.get("streak",0)+1
    else: state["streak"]=1
    state["best_streak"]=max(state.get("best_streak",0),state["streak"])
    state["quality_tier"]=qs["tier"]; state["quality_score"]=qs; state["last_contribution_date"]=_now_iso()
    xp_earned=int(qs["overall"]*1.5); state["total_xp"]=state.get("total_xp",0)+xp_earned; state["level"]=_level_for_xp(state["total_xp"])
    badge=_badge_for_state(state)
    if badge and badge not in state["badges"]: state["badges"].append(badge)
    missions_awarded=[]; flags=state.setdefault("mission_flags",{}); total_subs=flags.get("total_submissions",0)+1; flags["total_submissions"]=total_subs
    pathways=set(flags.get("pathways",[])); pathways.add(req.pathway); flags["pathways"]=list(pathways)
    pc=flags.setdefault("pathway_counts",{}); pc[req.pathway]=pc.get(req.pathway,0)+1; flags["pathway_counts"]=pc
    
    # Track submission type
    sub_type = req.submission_type
    type_counts = flags.setdefault("submission_type_counts",{})
    type_counts[sub_type] = type_counts.get(sub_type,0)+1
    flags["submission_type_counts"]=type_counts
    
    # Track sources contributed
    if req.source and req.source not in state.get("sources_contributed",[]):
        state.setdefault("sources_contributed",[]).append(req.source)
    
    # Track tags
    if req.tags:
        all_tags = set(state.get("tags",[]))
        all_tags.update(req.tags)
        state["tags"] = list(all_tags)
    
    # Track verified contributions
    if req.verified:
        state["verifications"]=state.get("verifications",0)+1
        if "verified_contributions" not in flags: flags["verified_contributions"]=[]
        flags["verified_contributions"].append({"source":req.source,"type":sub_type,"timestamp":_now_iso()})
    for m in MISSION_CATALOG:
        mid=m["id"]
        if mid in flags.get("earned",[]): continue
        award=False
        if mid=="first_spark" and total_subs==1: award=True
        elif mid=="streak_7" and state["streak"]>=7: award=True
        elif mid=="streak_30" and state["streak"]>=30: award=True
        elif mid=="verified" and qs["tier"]=="verified": award=True
        elif mid=="data_steward" and total_subs>=5: award=True
        elif mid=="sector_pioneer" and len(pathways)>=4: award=True
        elif mid=="community_voice" and total_subs>=10: award=True
        elif mid=="data_architect" and len(new_sources_added)>=1: award=True
        elif mid=="researcher" and state.get("interviews_completed",0)>=3: award=True
        elif mid=="governor" and state.get("gov_contributions",0)>=1: award=True
        elif mid=="community_builder" and total_subs>=20: award=True
        elif mid=="source_master" and len(state.get("sources_contributed",[]))>=5: award=True
        elif mid=="quality_guardian" and state.get("verifications",0)>=10: award=True
        elif mid=="mentor" and state.get("mentees_helped",0)>=1: award=True
        elif mid=="explorer_visit" and len(state.get("pages_visited",[]))>=7: award=True
        elif mid=="legacy_builder" and len(state.get("categories_contributed",[]))>=11: award=True
        # Constituency-specific missions
        elif mid=="business_expert" and state.get("pathway_counts",{}).get("B",0)>=3: award=True
        elif mid=="community_champion" and state.get("pathway_counts",{}).get("C",0)>=5: award=True
        elif mid=="visitor_insights" and state.get("pathway_counts",{}).get("D",0)>=3: award=True
        elif mid=="industry_leader" and state.get("pathway_counts",{}).get("E",0)>=2: award=True
        elif mid=="multi_constituency" and sum(state.get("pathway_counts",{}).values())>=10: award=True
        # Infrastructure & Code missions
        elif mid=="code_committer" and state.get("prs_merged",0)>=1: award=True
        elif mid=="infrastructure_builder" and state.get("infra_fixes",0)>=1: award=True
        elif mid=="ci_cd_contributor" and state.get("ci_improvements",0)>=1: award=True
        elif mid=="test_contributor" and state.get("tests_added",0)>=1: award=True
        elif mid=="doc_contributor" and state.get("docs_improved",0)>=1: award=True
        elif mid=="review_contributor" and state.get("prs_reviewed",0)>=5: award=True
        elif mid=="analyst" and state["total_xp"]>=500: award=True
        elif mid=="architect" and state["total_xp"]>=5000: award=True
        elif mid=="visionary" and state["total_xp"]>=10000: award=True
        elif mid=="data_architect" and len(new_sources_added)>=1: award=True
        elif mid=="researcher" and state.get("interviews_completed",0)>=3: award=True
        elif mid=="governor" and state.get("gov_contributions",0)>=1: award=True
        elif mid=="community_builder" and total_subs>=20: award=True
        elif mid=="source_master" and len(state.get("sources_contributed",[]))>=5: award=True
        elif mid=="quality_guardian" and state.get("verifications",0)>=10: award=True
        elif mid=="mentor" and state.get("mentees_helped",0)>=1: award=True
        elif mid=="explorer_visit" and len(state.get("pages_visited",[]))>=7: award=True
        elif mid=="legacy_builder" and len(state.get("categories_contributed",[]))>=11: award=True
        elif mid=="analyst" and state["total_xp"]>=500: award=True
        elif mid=="architect" and state["total_xp"]>=5000: award=True
        elif mid=="visionary" and state["total_xp"]>=10000: award=True
        # Civic & Community Engagement missions (Tier 6)
        elif mid=="civic_participant" and state.get("civic_events_attended",0)>=1: award=True
        elif mid=="data_citizen" and state.get("data_points_verified",0)>=5: award=True
        elif mid=="open_intelligence_advocate" and state.get("shares_count",0)>=10: award=True
        elif mid=="transparency_champion" and state.get("foia_requests",0)>=3: award=True
        elif mid=="policy_contributor" and state.get("policy_recommendations",0)>=1: award=True
        elif mid=="budget_analyst" and state.get("budget_docs_analyzed",0)>=3: award=True
        elif mid=="census_participant" and state.get("census_completed",False): award=True
        elif mid=="community_organizer" and state.get("data_drives_coordinated",0)>=3: award=True
        elif mid=="youth_mentor" and state.get("students_mentored",0)>=1: award=True
        elif mid=="senior_advisor" and state.get("pathway_counts",{}).get("K",0)>=1: award=True
        # Environmental & Public Health Stewardship (Tier 7)
        elif mid=="environmental_steward" and state.get("pathway_counts",{}).get("Q",0)>=5: award=True
        elif mid=="climate_analyst" and state.get("climate_observations",0)>=3: award=True
        elif mid=="public_health_advocate" and state.get("pathway_counts",{}).get("M",0)>=3: award=True
        elif mid=="safety_reporter" and state.get("pathway_counts",{}).get("P",0)>=5: award=True
        elif mid=="agriculture_steward" and state.get("pathway_counts",{}).get("N",0)>=3: award=True
        elif mid=="water_quality_monitor" and state.get("water_quality_observations",0)>=3: award=True
        # Research & Data Science (Tier 8)
        elif mid=="data_scientist" and state.get("visualizations_built",0)>=1: award=True
        elif mid=="statistical_modeler" and state.get("predictive_models",0)>=1: award=True
        elif mid=="geospatial_analyst" and state.get("geo_layers_added",0)>=1: award=True
        elif mid=="corpus_builder" and state.get("structured_data_points",0)>=100: award=True
        elif mid=="open_data_curator" and state.get("datasets_published",0)>=1: award=True
        elif mid=="api_developer" and state.get("api_integrations_built",0)>=1: award=True
        # Governance & Institutional Impact (Tier 9)
        elif mid=="board_advisor" and state.get("presentations_to_board",0)>=1: award=True
        elif mid=="grant_writer" and state.get("grants_secured",0)>=1: award=True
        elif mid=="institutional_partner" and state.get("institutional_partnerships",0)>=1: award=True
        elif mid=="policy_influencer" and state.get("policy_citations",0)>=1: award=True
        # Tier 10 — Legend
        elif mid=="legend" and state["total_xp"]>=50000: award=True
        elif mid=="founder" and state.get("joined_date","") < "2026-09-01": award=True
        if award:
            flags.setdefault("earned",[]).append(mid); missions_awarded.append({"mission_id":mid,"name":m["name"],"xp_awarded":m["xp"],"new_total_xp":state["total_xp"],"new_level":state["level"]}); state["total_xp"]+=m["xp"]; state["level"]=_level_for_xp(state["total_xp"])
    entry={"date":_now_iso(),"contributor":cid,"type":req.pathway,"quality_score":qs["overall"],"quality_tier":qs["tier"],"status":"accepted","reviewed_by":"automated","xp_earned":xp_earned,"missions":[m["mission_id"] for m in missions_awarded]}
    _contributions.append(entry); _save_state(cid)
    return {"contributor_id":cid,"pathway":req.pathway,"quality_score":qs,"quality_tier":qs["tier"],"streak":state["streak"],"best_streak":state["best_streak"],"badges":state["badges"],"missions_awarded":missions_awarded,"total_xp":state["total_xp"],"level":state["level"],"status":"accepted","computed_at":_now_iso()}
@router.get("/quality")
def get_quality(contributor_id=Query(...),pathway=Query("data_source")):
    state=_gam_state.get(contributor_id,{}); qs=state.get("quality_score",{})
    if not qs: return {"contributor_id":contributor_id,"quality_score":None,"quality_tier":QualityTier.PENDING.value}
    return {"contributor_id":contributor_id,"quality_score":qs,"quality_tier":qs.get("tier",QualityTier.PENDING.value),"pathway":pathway,"computed_at":state.get("last_contribution_date","")}
@router.get("/reputation/{contributor_id}")
def get_reputation(contributor_id):
    state=_load_state(contributor_id); total=sum(1 for c in _contributions if c.get("contributor")==contributor_id); accepted=sum(1 for c in _contributions if c.get("contributor")==contributor_id and c.get("status")=="accepted"); accuracy=round(accepted/max(total,1),3); badges=list(state.get("badges",[]))
    if not badges:
        b=_badge_for_state(state)
        if b: badges.append(b)
    flags=state.get("mission_flags",{})
    return {"contributor_id":contributor_id,"verified_contributions":accepted,"total_submissions":total,"accuracy_rate":accuracy,"current_streak":state.get("streak",0),"best_streak":state.get("best_streak",0),"quality_tier":state.get("quality_tier",QualityTier.PENDING.value),"badges":badges,"total_xp":state.get("total_xp",0),"level":state.get("level","Newcomer"),"contribution_count_by_pathway":flags.get("pathways",[])}
@router.get("/leaderboard")
def get_leaderboard(pathway=Query("all"),period=Query("weekly"),limit=Query(10)):
    entries=[]
    for cid,state in _gam_state.items():
        qs=state.get("quality_score",{})
        entries.append({"contributor_id":cid,"score":state.get("total_xp",qs.get("overall",0.0)),"verified_contributions":state.get("streak",0),"accuracy_rate":0.0,"current_streak":state.get("streak",0),"quality_tier":state.get("quality_tier",QualityTier.PENDING.value),"level":state.get("level","Newcomer"),"total_xp":state.get("total_xp",0)})
    entries.sort(key=lambda e:(e["total_xp"],e["quality_tier"]),reverse=True)
    for i,e in enumerate(entries[:limit],1): e["rank"]=i
    if period=="weekly": _save_leaderboard_snapshot(entries[:limit])
    return {"period":period,"pathway":pathway,"entries":entries,"computed_at":_now_iso()}
@router.get("/missions")
def get_missions(contributor_id=Query(...)):
    state=_load_state(contributor_id); flags=state.get("mission_flags",{}); earned=set(flags.get("earned",[])); results=[]
    for m in MISSION_CATALOG: results.append({"mission_id":m["id"],"name":m["name"],"status":"earned" if m["id"] in earned else "available","xp":m["xp"]})
    return {"missions":results,"available":MISSION_CATALOG}
@router.post("/resync")
def resync():
    global _gam_state
    for f in GAMIFICATION_DIR.glob("*.json"):
        try: _gam_state[f.stem]=json.loads(f.read_text())
        except Exception: continue
    return {"status":"resynced","contributors":len(_gam_state)}
@router.get("/pulse")
def get_pulse(hours_threshold=Query(48)):
    items=[]
    for f in sorted(GAMIFICATION_DIR.glob("*.json")):
        try: data=json.loads(f.read_text())
        except Exception: continue
        if not isinstance(data,dict): continue
        for key,val in data.items():
            if key in ("source","sourceUrl","vintage","fetchedAt"): continue
            if isinstance(val,(int,float)): items.append({"indicator_id":f"{f.stem}.{key}","name":key,"category":f.stem,"old_value":float(val),"new_value":float(val),"delta_pct":0.0,"direction":"stable","source":f.stem,"stale_hours":hours_threshold})
            elif isinstance(val,dict):
                for ik,iv in val.items():
                    if isinstance(iv,(int,float)): items.append({"indicator_id":f"{f.stem}.{key}.{ik}","name":ik,"category":f.stem,"old_value":float(iv),"new_value":float(iv),"delta_pct":0.0,"direction":"stable","source":f.stem,"stale_hours":hours_threshold})
    return {"items":items[:50],"generated_at":_now_iso()}
@router.get("/profile/{contributor_id}")
def get_profile(contributor_id):
    rep=get_reputation(contributor_id); state=_load_state(contributor_id); contributions=[c for c in _contributions if c.get("contributor")==contributor_id]
    return {"contributor_id":contributor_id,"reputation":rep,"contributions":contributions,"current_streak":state.get("streak",0),"best_streak":state.get("best_streak",0),"badges":state.get("badges",[]),"joined_date":state.get("joined_date",""),"quality_tier":state.get("quality_tier",QualityTier.PENDING.value),"total_xp":state.get("total_xp",0),"level":state.get("level","Newcomer"),"missions":state.get("mission_flags",{}).get("earned",[])}
