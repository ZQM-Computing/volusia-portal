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
    {"id":"first_spark","name":"First Spark","desc":"Submit your first contribution","xp":50},
    {"id":"streak_7","name":"Streak 7","desc":"7-day contribution streak","xp":100},
    {"id":"streak_30","name":"Streak 30","desc":"30-day contribution streak","xp":250},
    {"id":"verified","name":"Verified Contributor","desc":"Reach Verified quality tier","xp":200},
    {"id":"data_steward","name":"Data Steward","desc":"5+ accepted submissions","xp":300},
    {"id":"sector_pioneer","name":"Sector Pioneer","desc":"Submit in all 4 constituencies","xp":400},
    {"id":"community_voice","name":"Community Voice","desc":"10+ total contributions","xp":150},
    {"id":"analyst","name":"Analyst","desc":"Reach Analyst level (500 XP)","xp":0},
    {"id":"architect","name":"Architect","desc":"Reach Architect level (5000 XP)","xp":0},
]
class QualityTier(str, Enum):
    VERIFIED="verified"; REVIEWED="reviewed"; PENDING="pending"; FLAGGED="flagged"
class ContributeRequest(BaseModel):
    contributor_id: str
    pathway: str = Field(..., pattern=r"^[A-Ia-i]$|^agent-item$")
    submission: dict = Field(default_factory=dict)
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
    return _gam_state.setdefault(cid,{"total_xp":0,"level":"Newcomer","streak":0,"best_streak":0,"quality_tier":QualityTier.PENDING.value,"quality_score":{},"badges":[],"joined_date":_now_iso(),"last_contribution_date":_now_iso(),"last_seen_values":{},"review_velocity_days":3.0,"mission_flags":{}})
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
        elif mid=="analyst" and state["total_xp"]>=500: award=True
        elif mid=="architect" and state["total_xp"]>=5000: award=True
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
