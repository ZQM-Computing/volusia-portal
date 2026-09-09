#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "=== Project Volusia — Refresh Data ==="
echo ""

# Refresh backend
echo "Triggering backend refresh..."
curl -s -X POST http://localhost:8000/refresh \
    -H "Content-Type: application/json" \
    -d '{"secret":"'$(grep VOLUSIA_REFRESH_TOKEN .env.example 2>/dev/null | cut -d= -f2)"'"}' 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "(refresh endpoint may need auth)"

# Run refresh_v2.py pipeline
echo ""
echo "Running refresh_v2.py pipeline..."
cd scripts && python3 refresh_v2.py 2>&1 | tail -20
cd ..

echo ""
echo "✓ Data refresh complete"
echo "  Check: curl http://localhost:8000/health"
