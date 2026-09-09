#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "=== Project Volusia — Full Dev Environment ==="
echo ""

# Start backend if not running
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "Starting backend (uvicorn)..."
    cd backend && nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload > /dev/null 2>&1 &
    cd ..
    sleep 2
fi
STATUS=$(curl -s http://localhost:8000/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['status'])")
COUNT=$(curl -s http://localhost:8000/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['indicator_count'])")
echo "✓ Backend :8000 — ${STATUS} (${COUNT} indicators)"

# Start nginx if not running
if ! curl -s http://localhost:8089 > /dev/null 2>&1; then
    echo "Starting nginx..."
    nssm start Volusia-Nginx 2>/dev/null || echo "  (nginx may already be running)"
fi
echo "✓ Nginx :8089 — serving static files"

# Start cloudflared if zqmlabs.com not responding
if ! curl -s https://zqmlabs.com > /dev/null 2>&1; then
    echo "Starting cloudflared tunnel..."
    nssm start cloudflared 2>/dev/null || echo "  (tunnel may already be running)"
fi
echo "✓ cloudflared — zqmlabs.com"

echo ""
echo "=== All services running! ==="
echo "  Live site: https://zqmlabs.com"
echo "  API:       http://localhost:8000/health"
echo "  Dev:       http://localhost:5173 (npm run dev)"
echo "  Nginx:     http://localhost:8089"
echo ""
