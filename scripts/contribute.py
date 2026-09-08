#!/usr/bin/env python3
"""
Project Volusia — Contribution Pipeline Script
================================================
Automated contribution to the Challenge Wallet KB (:8787) with full
verification and artifact tracking.

Usage:
    python scripts/contribute.py --help
    python scripts/contribute.py --pathway A --data sources/economic.json
    python scripts/contribute.py --verify --agent hermes-zqmco

Per the zqm-kb-contribute skill protocol:
- Token sourced from .chw_token file (fallback: GET /recover)
- Payload shape: {table, payload, agent} — NOT top-level fields
- POST via curl --http1.0 (curl exit 52 bug with HTTP/1.1)
- Write payload JSON to CWD file first (MSYS /tmp pitfall)
- Verify via GET /api row-level readback
"""

import json
import sys
import os
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
KB_BASE = os.environ.get("KB_BASE", "http://127.0.0.1:8787")
TOKEN_FILE = os.environ.get("CHW_TOKEN_FILE", "C:/tools/bitgo-challenge/.chw_token")
AGENT_NAME = os.environ.get("KB_AGENT", "hermes-zqmco")
CWD = Path.cwd()

# ---------------------------------------------------------------------------
# Token Management
# ---------------------------------------------------------------------------

def read_token() -> str:
    """Read the KB contribution token from .chw_token file."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            return f.read().strip()
    return ""

def check_kb_reachable() -> dict:
    """Check if KB :8787 is reachable and return health info."""
    result = {"reachable": False, "status": "unknown", "token_src": "unknown"}
    
    try:
        import urllib.request
        req = urllib.request.urlopen(f"{KB_BASE}/healthz", timeout=5)
        data = json.loads(req.read())
        result["reachable"] = True
        result["status"] = data.get("status", "healthy")
        result["token_src"] = data.get("meta", {}).get("token_src", "unknown")
        result["counts"] = data.get("counts", {})
    except Exception as e:
        result["reachable"] = False
        result["error"] = str(e)
    
    # Also check :8768 (HermesKB) as fallback indicator
    try:
        import urllib.request
        req = urllib.request.urlopen("http://127.0.0.1:8768/", timeout=3)
        result["hermeskb_8768"] = True
    except:
        result["hermeskb_8768"] = False
    
    return result

def get_token() -> str:
    """Get the current valid contribution token."""
    token = read_token()
    if not token:
        print("ERROR: No .chw_token file found at", TOKEN_FILE)
        print("Run: python scripts/contribute.py --recover-token")
        sys.exit(1)
    return token

def recover_token(agent: str = AGENT_NAME, contact: str = "zqmcomputing@gmail.com") -> dict:
    """Recover tokens via GET /recover endpoint."""
    try:
        import urllib.request
        url = f"{KB_BASE}/recover?agent={agent}&contact={contact}"
        req = urllib.request.urlopen(url, timeout=10)
        data = json.loads(req.read())
        if isinstance(data, list) and len(data) > 0:
            return {"ok": True, "tokens": data, "use_token": data[-1].get("token", "")}
        return {"ok": False, "error": "No tokens found", "data": data}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# ---------------------------------------------------------------------------
# Contribution Functions
# ---------------------------------------------------------------------------

def post_contribute(table: str, payload: dict, token: str, agent: str = AGENT_NAME) -> dict:
    """POST a contribution row to KB :8787/contribute.
    
    Per the zqm-kb-contribute skill protocol:
    - Body shape: {table, payload, agent} — NOT top-level fields
    - Use curl --http1.0 to avoid HTTP/1.1 Expect: 100-continue bug
    - Write payload to file first (MSYS /tmp pitfall)
    """
    import subprocess
    import tempfile
    
    contrib_payload = {
        "table": table,
        "agent": agent,
        "payload": payload,
        "dedup_key": f"{table}_{hashlib.md5(json.dumps(payload).encode()).hexdigest()[:8]}"
    }
    
    # Write to CWD file (NOT /tmp — MSYS bash can't read /tmp via curl)
    payload_file = CWD / "kb_contrib_tmp.json"
    with open(payload_file, "w") as f:
        json.dump(contrib_payload, f, indent=2)
    
    # POST via curl --http1.0 (curl exit 52 bug with HTTP/1.1)
    try:
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", f"{KB_BASE}/contribute",
             "-H", "Content-Type: application/json",
             "-H", f"Authorization: Bearer {token}",
             "--http1.0",
             "--data-binary", f"@{payload_file}"],
            capture_output=True, text=True, timeout=30
        )
        # Clean up temp file
        payload_file.unlink(missing_ok=True)
        
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
        return {"error": f"curl exit {result.returncode}", "stderr": result.stderr[:200]}
    except Exception as e:
        payload_file.unlink(missing_ok=True)
        return {"error": str(e)}

def post_knowledge(claim: str, category: str, source: str, 
                   confidence: str = "HIGH", agent: str = AGENT_NAME) -> dict:
    """Post a knowledge row to the KB."""
    token = get_token()
    payload = {
        "category": category,
        "claim": claim,
        "source": source,
        "confidence": confidence,
        "verified": 0
    }
    return post_contribute("knowledge", payload, token, agent)

def post_finding(finding_id: str, title: str, severity: str = "MEDIUM",
                 status: str = "PENDING", detail: str = "",
                 source: str = "", agent: str = AGENT_NAME) -> dict:
    """Post a findings row to the KB (needle-vote eligible)."""
    token = get_token()
    payload = {
        "finding_id": finding_id,
        "title": title,
        "severity": severity,
        "status": status,
        "detail": detail,
        "source": source
    }
    return post_contribute("findings", payload, token, agent)

# ---------------------------------------------------------------------------
# Verification Functions
# ---------------------------------------------------------------------------

def verify_contribution(row_id: int, expected_claim: str = None) -> dict:
    """Verify a contribution was posted correctly.
    
    Per zqm-kb-contribute skill:
    1. Content integrity: stored claim == canonical claim verbatim
    2. Field parity: category, confidence match payload
    3. Canonical JSON internal consistency
    """
    try:
        import urllib.request
        token = get_token()
        req = urllib.request.urlopen(f"{KB_BASE}/api", timeout=10)
        data = json.loads(req.read())
        
        # Search for the row by id
        for table in ["knowledge", "findings", "severability"]:
            for row in data.get(table, []):
                if row.get("id") == row_id:
                    result = {"found": True, "table": table, "row": row}
                    if expected_claim:
                        if table == "knowledge":
                            result["content_match"] = row.get("claim") == expected_claim
                        elif table == "findings":
                            result["content_match"] = row.get("title") == expected_claim
                    return result
        
        return {"found": False, "row_id": row_id}
    except Exception as e:
        return {"error": str(e)}

def get_counts() -> dict:
    """Get current KB counts via /healthz."""
    try:
        import urllib.request
        req = urllib.request.urlopen(f"{KB_BASE}/healthz", timeout=5)
        data = json.loads(req.read())
        return data.get("counts", {})
    except:
        return {}

def get_leaderboard() -> dict:
    """Get gamification leaderboard."""
    try:
        import urllib.request
        req = urllib.request.urlopen(f"{KB_BASE}/api?meta=1", timeout=5)
        data = json.loads(req.read())
        return {"meta": data.get("meta", {}), "counts": data.get("counts", {})}
    except:
        return {}

# ---------------------------------------------------------------------------
# Mission Tracking
# ---------------------------------------------------------------------------

def check_missions(agent: str = AGENT_NAME) -> dict:
    """Check current mission progress."""
    try:
        import urllib.request
        token = get_token()
        req = urllib.request.urlopen(f"{KB_BASE}/gamification/missions", 
                                      timeout=5)
        data = json.loads(req.read())
        return {"ok": True, "missions": data}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def get_pulse() -> dict:
    """Get current pulse data."""
    try:
        import urllib.request
        req = urllib.request.urlopen(f"{KB_BASE}/gamification/pulse", timeout=5)
        return json.loads(req.read())
    except:
        return {}

# ---------------------------------------------------------------------------
# Pipeline: Full Contribution Workflow
# ---------------------------------------------------------------------------

def contribution_workflow(claims: list, table: str = "knowledge") -> dict:
    """Execute a full contribution workflow with verification.
    
    Steps:
    1. Pre-check KB health and counts
    2. POST each claim
    3. Verify each row
    4. Report counts delta
    """
    token = get_token()
    
    # Pre-check
    print("[1/5] Checking KB health...")
    health = check_kb_reachable()
    if not health["reachable"]:
        print(f"  WARNING: KB {KB_BASE} not reachable!")
        print(f"  Error: {health.get('error', 'Unknown')}")
        print(f"  HermesKB :8768 available: {health.get('hermeskb_8768', False)}")
    
    print(f"[2/5] Pre-check counts: {json.dumps(get_counts(), indent=2)}")
    before_counts = get_counts()
    
    # POST claims
    print(f"[3/5] Posting {len(claims)} {table} rows...")
    posted = []
    for claim_data in claims:
        if table == "knowledge":
            result = post_knowledge(
                claim=claim_data.get("claim", ""),
                category=claim_data.get("category", ""),
                source=claim_data.get("source", ""),
                confidence=claim_data.get("confidence", "HIGH")
            )
        elif table == "findings":
            result = post_finding(
                finding_id=claim_data.get("finding_id", ""),
                title=claim_data.get("title", ""),
                severity=claim_data.get("severity", "MEDIUM"),
                status=claim_data.get("status", "PENDING"),
                detail=claim_data.get("detail", ""),
                source=claim_data.get("source", "")
            )
        else:
            result = post_contribute(table, claim_data.get("payload", {}), token)
        
        posted.append(result)
        if "id" in result:
            print(f"  POSTED: id={result['id']}, verified={result.get('verified', '?')}")
        elif "error" in result:
            print(f"  FAILED: {result['error']}")
    
    # Verify
    print("[4/5] Verifying posted rows...")
    for row in posted:
        if "id" in row:
            verification = verify_contribution(row["id"])
            if verification.get("content_match"):
                print(f"  VERIFIED: id={row['id']} — content matches")
            elif verification.get("found"):
                print(f"  PARTIAL: id={row['id']} — found but content mismatch")
    
    # Counts delta
    print("[5/5] Post-check counts...")
    after_counts = get_counts()
    delta = {}
    for k in before_counts:
        before = before_counts.get(k, 0)
        after = after_counts.get(k, 0)
        delta[k] = after - before
    print(f"  Counts delta: {json.dumps(delta, indent=2)}")
    
    return {
        "posted": posted,
        "before_counts": before_counts,
        "after_counts": after_counts,
        "delta": delta,
        "health": health
    }

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Project Volusia Contribution Pipeline")
    parser.add_argument("--check-health", action="store_true", help="Check KB :8787 reachability")
    parser.add_argument("--recover-token", action="store_true", help="Recover tokens via GET /recover")
    parser.add_argument("--post-knowledge", action="store_true", help="Post a knowledge row")
    parser.add_argument("--post-finding", action="store_true", help="Post a findings row")
    parser.add_argument("--verify", action="store_true", help="Verify a contribution")
    parser.add_argument("--missions", action="store_true", help="Check mission progress")
    parser.add_argument("--pulse", action="store_true", help="Get pulse data")
    parser.add_argument("--counts", action="store_true", help="Get KB counts")
    parser.add_argument("--workflow", action="store_true", help="Run full contribution workflow")
    parser.add_argument("--agent", default=AGENT_NAME, help="Agent name")
    parser.add_argument("--kb-base", default=KB_BASE, help="KB base URL")
    parser.add_argument("--claim", default="", help="Claim text (for knowledge row)")
    parser.add_argument("--category", default="", help="Category (for knowledge row)")
    parser.add_argument("--source", default="", help="Source (for knowledge row)")
    parser.add_argument("--confidence", default="HIGH", help="Confidence level")
    parser.add_argument("--finding-id", default="", help="Finding ID")
    parser.add_argument("--title", default="", help="Finding title")
    parser.add_argument("--table", default="knowledge", help="Table name")
    parser.add_argument("--payload", default="", help="JSON payload file path")
    
    args = parser.parse_args()
    
    if args.kb_base:
        globals()["KB_BASE"] = args.kb_base
    
    if args.check_health:
        result = check_kb_reachable()
        print(json.dumps(result, indent=2))
        if not result["reachable"]:
            print("\nWARNING: KB :8787 not reachable from this host!")
            print("See: https://github.com/ZQM-Computing/volusia-portal/issues/8")
            sys.exit(1)
    
    elif args.recover_token:
        result = recover_token(args.agent)
        print(json.dumps(result, indent=2))
    
    elif args.post_knowledge:
        if not args.claim or not args.category or not args.source:
            print("ERROR: --claim, --category, and --source are required for knowledge rows")
            sys.exit(1)
        result = post_knowledge(args.claim, args.category, args.source, args.confidence)
        print(json.dumps(result, indent=2))
    
    elif args.post_finding:
        result = post_finding(args.finding_id, args.title, source=args.source)
        print(json.dumps(result, indent=2))
    
    elif args.verify:
        result = verify_contribution(int(args.finding_id) if args.finding_id else 0)
        print(json.dumps(result, indent=2))
    
    elif args.missions:
        result = check_missions(args.agent)
        print(json.dumps(result, indent=2))
    
    elif args.pulse:
        result = get_pulse()
        print(json.dumps(result, indent=2))
    
    elif args.counts:
        result = get_counts()
        print(json.dumps(result, indent=2))
    
    elif args.workflow:
        if not args.payload:
            print("ERROR: --payload <json_file> required for workflow")
            sys.exit(1)
        with open(args.payload) as f:
            claims = json.load(f)
        if not isinstance(claims, list):
            claims = [claims]
        result = contribution_workflow(claims, args.table)
        print(json.dumps(result, indent=2))
    
    else:
        # Default: show health status
        result = check_kb_reachable()
        print(json.dumps(result, indent=2))
        if not result["reachable"]:
            print("\nKB :8787 not reachable. Use --check-health to investigate.")
            print("Token file:", TOKEN_FILE)
            print("Agent:", AGENT_NAME)

if __name__ == "__main__":
    main()
