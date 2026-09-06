#!/bin/bash
# Project Volusia — Automated Refresh and Diagnostics
# Runs every hour via crontab

cd "$(dirname "$0")/.." || exit 1

echo "=== Refresh started at $(date) ==="

# Trigger backend refresh
curl -s http://localhost:8000/refresh > /dev/null 2>&1

# Run diagnostics
curl -s http://localhost:8000/diagnostics | python3 -c "
import sys, json
d = json.load(sys.stdin)
status = d.get('overall', 'unknown')
checks = d.get('checks', {})
print(f'Status: {status}')
print(f'  Database: {checks.get(\"database\", \"?\")}')
print(f'  API: {checks.get(\"api_endpoints\", \"?\")}')
print(f'  Gamification: {checks.get(\"gamification\", \"?\")}')
print(f'  Map Layers: {checks.get(\"map_layers\", \"?\")}')
if status != 'healthy':
    print('ALERT: System degraded!')
" 2>/dev/null

# Rebuild frontend if needed
if [ ! -d "dist" ]; then
    echo "Frontend dist missing, rebuilding..."
    npm run build 2>&1
fi

echo "=== Refresh completed at $(date) ==="
