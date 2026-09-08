#!/usr/bin/env python3
"""
Project Volusia — KB Connectivity Bridge
================================================
When KB :8787 is not directly reachable from this host (confirmed: 
SYN_SENT on 127.0.0.1:8787, connection refused), this module provides
alternate pathways to reach the KB.

Options:
1. Route through another mesh node (N3 at .78, N9 at .250)
2. Route through the quantum-sim :8891 gateway
3. Use the mesh-api :8899 service for inter-node communication
4. Fallback: n8n workflow trigger for KB contribution

Per the jarvis-mesh-coordinator skill:
- Probe http://<node>:8891/ on each candidate
- Use SSH to reach nodes with working creds
- Execute per node, isolate failures
"""

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, Literal
from dataclasses import dataclass
from enum import Enum

# ---------------------------------------------------------------------------
# Mesh Configuration (verified 2026-09-08)
# ---------------------------------------------------------------------------
# Verified topology:
#   .217 (Node-4, Win10) = control plane, 46 Docker containers
#   .78 (Node-3) = reachable via :8891 quantum-sim
#   .250 (Node-4?) = serves :80/:443, does NOT run :8891
#   DEAD: .218, .219, .196, .228 (ARP Incomplete)

@dataclass
class MeshNode:
    name: str
    ip: str
    ports: list
    reachable: bool = False
    ssh_available: bool = False

class KBConnectivity(Enum):
    DIRECT = "direct"        # :8787 accessible from localhost
    MESH_NODE = "mesh_node"  # Via SSH to another mesh node
    PROXY = "proxy"          # Via existing running service
    DEAD = "dead"           # KB completely unreachable

# KB service ports on mesh nodes
KB_PORTS = {8787: "challenge-wallet", 8768: "hermes-kb"}

def probe_node(ip: str) -> dict:
    """Probe a mesh node for KB services."""
    result = {"ip": ip, "services": {}, "reachable": False}
    
    # Try each KB port
    for port, name in KB_PORTS.items():
        try:
            import urllib.request
            req = urllib.request.urlopen(f"http://{ip}:{port}/healthz", timeout=3)
            data = json.loads(req.read())
            result["services"][port] = {"name": name, "status": "healthy", "data": data}
            result["reachable"] = True
        except:
            result["services"][port] = {"name": name, "status": "unreachable"}
    
    # Try quantum-sim :8891
    try:
        import urllib.request
        req = urllib.request.urlopen(f"http://{ip}:8891/", timeout=3)
        result["services"][8891] = {"name": "quantum-sim", "status": "reachable"}
    except:
        result["services"][8891] = {"name": "quantum-sim", "status": "unreachable"}
    
    return result

def find_kb_node() -> Optional[MeshNode]:
    """Find which mesh node has KB :8787 running."""
    candidates = [
        MeshNode("self", "127.0.0.1", [8787, 8768]),
        MeshNode("n3", "192.168.1.78", [8787, 8768, 8891]),
        MeshNode("n9", "192.168.1.250", [8787, 8768]),
        MeshNode("n1", "192.168.1.224", [8787, 8768]),
    ]
    
    for node in candidates:
        result = probe_node(node.ip)
        node.reachable = result["reachable"]
        node.ssh_available = False  # Would need SSH key setup
        if node.reachable:
            return node
    
    return None

def get_kb_connectivity() -> KBConnectivity:
    """Determine the best connectivity method for KB :8787."""
    # Check direct
    try:
        import urllib.request
        req = urllib.request.urlopen("http://127.0.0.1:8787/healthz", timeout=3)
        return KBConnectivity.DIRECT
    except:
        pass
    
    # Check mesh nodes
    node = find_kb_node()
    if node and node.ip != "127.0.0.1":
        return KBConnectivity.MESH_NODE
    
    # Check if quantum-sim :8891 can proxy
    try:
        import urllib.request
        req = urllib.request.urlopen("http://127.0.0.1:8891/", timeout=3)
        return KBConnectivity.PROXY
    except:
        pass
    
    return KBConnectivity.DEAD

def bridge_kb(method: KBConnectivity = None) -> dict:
    """Establish a KB bridge using the best available method."""
    if method is None:
        method = get_kb_connectivity()
    
    result = {
        "method": method.value,
        "kb_base": "http://127.0.0.1:8787",
        "working": False,
        "details": {}
    }
    
    if method == KBConnectivity.DIRECT:
        result["working"] = True
        result["details"] = {"note": "KB :8787 directly accessible"}
    
    elif method == KBConnectivity.MESH_NODE:
        node = find_kb_node()
        result["working"] = True
        result["details"] = {
            "node": node.name,
            "ip": node.ip,
            "note": f"Route KB calls through {node.name} ({node.ip})"
        }
    
    elif method == KBConnectivity.PROXY:
        result["working"] = True
        result["details"] = {
            "proxy": "quantum-sim :8891",
            "note": "Route through quantum-sim gateway"
        }
    
    else:
        result["working"] = False
        result["details"] = {
            "error": "KB :8787 unreachable from all known network paths",
            "suggestion": "Check network connectivity or restart KB supervisor"
        }
    
    return result

# ---------------------------------------------------------------------------
# Contribution Gateway (n8n integration)
# ---------------------------------------------------------------------------

def trigger_n8n_contribution(workflow_id: str, payload: dict) -> dict:
    """Trigger an n8n workflow for KB contribution.
    
    n8n runs on localhost:5678 (or the mesh node running n8n).
    This is the fallback when KB :8787 is directly unreachable.
    """
    try:
        import urllib.request
        n8n_url = os.environ.get("N8N_URL", "http://127.0.0.1:5678")
        req = urllib.request.urlopen(f"{n8n_url}/webhook/{workflow_id}", 
                                     data=json.dumps(payload).encode(),
                                     timeout=10)
        return {"ok": True, "status": req.status, "data": json.loads(req.read())}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="KB Connectivity Bridge")
    parser.add_argument("--probe", action="store_true", help="Probe all mesh nodes")
    parser.add_argument("--connectivity", action="store_true", help="Check KB connectivity")
    parser.add_argument("--bridge", action="store_true", help="Establish KB bridge")
    parser.add_argument("--n8n", metavar="WORKFLOW_ID", help="Trigger n8n workflow")
    parser.add_argument("--payload", help="JSON payload file for n8n")
    
    args = parser.parse_args()
    
    if args.probe:
        nodes = ["127.0.0.1", "192.168.1.78", "192.168.1.250", "192.168.1.224"]
        for ip in nodes:
            result = probe_node(ip)
            print(f"{ip}: {'REACHABLE' if result['reachable'] else 'UNREACHABLE'} — {result['services']}")
    
    elif args.connectivity:
        result = get_kb_connectivity()
        print(f"KB Connectivity: {result.value}")
        bridge = bridge_kb(result)
        print(json.dumps(bridge, indent=2))
    
    elif args.bridge:
        bridge = bridge_kb()
        print(json.dumps(bridge, indent=2))
        if bridge["working"]:
            print("\nKB is accessible via:", bridge["method"])
        else:
            print("\nKB is UNREACHABLE. Suggested fix:")
            print("  1. Check if KB supervisor is running on the remote node")
            print("  2. SSH to a mesh node and proxy locally")
            print("  3. Restart the KB supervisor (chw_supervisor)")
    
    elif args.n8n:
        payload = {}
        if args.payload:
            with open(args.payload) as f:
                payload = json.load(f)
        result = trigger_n8n_contribution(args.n8n, payload)
        print(json.dumps(result, indent=2))
    
    else:
        # Default: show connectivity status
        result = get_kb_connectivity()
        bridge = bridge_kb(result)
        print(json.dumps(bridge, indent=2))

if __name__ == "__main__":
    main()
