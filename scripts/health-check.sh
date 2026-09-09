#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "═══════════════════════════════════════════════"
echo "  Project Volusia — Health Check"
echo "═══════════════════════════════════════════════"
echo ""

pass=0; fail=0

# Backend
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    STATUS=$(curl -s http://localhost:8000/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['status'])")
    COUNT=$(curl -s http://localhost:8000/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['indicator_count'])")
    echo "✓ Backend API :8000 — ${STATUS} (${COUNT} indicators)"
    ((pass++))
else
    echo "✗ Backend API :8000 — DOWN"
    ((fail++))
fi

# TypeScript
if npx tsc --noEmit > /dev/null 2>&1; then
    echo "✓ TypeScript compilation — PASS"
    ((pass++))
else
    echo "✗ TypeScript compilation — FAIL"
    ((fail++))
fi

# Live site
if curl -sL http://zqmlabs.com/ | grep -q "div id=\"root\""; then
    echo "✓ Live site zqmlabs.com — OK"
    ((pass++))
else
    echo "✗ Live site zqmlabs.com — DOWN"
    ((fail++))
fi

# Nginx
if pgrep -x nginx > /dev/null; then
    echo "✓ nginx process — RUNNING"
    ((pass++))
else
    echo "✗ nginx process — STOPPED"
    ((fail++))
fi

# cloudflared
if pgrep -x cloudflared > /dev/null; then
    echo "✓ cloudflared tunnel — RUNNING"
    ((pass++))
else
    echo "✗ cloudflared tunnel — STOPPED"
    ((fail++))
fi

# Employer DB
if sqlite3 data/volusia_employers.db "SELECT COUNT(*) FROM employers" > /dev/null 2>&1; then
    COUNT=$(sqlite3 data/volusia_employers.db "SELECT COUNT(*) FROM employers")
    echo "✓ Employer DB — ${COUNT} employers"
    ((pass++))
else
    echo "✗ Employer DB — MISSING"
    ((fail++))
fi

# Frontend dist
if [ -d "dist" ] && [ -f "dist/index.html" ]; then
    echo "✓ Frontend dist — BUILDED"
    ((pass++))
else
    echo "✗ Frontend dist — MISSING"
    ((fail++))
fi

echo ""
echo "Results: ${pass} passing, ${fail} failing"
echo "═══════════════════════════════════════════════"

[ "$fail" -eq 0 ]
