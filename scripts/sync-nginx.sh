#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "Building frontend..."
npm run build

echo "Syncing to nginx volume..."
cp dist/index.html ~/scoop/persist/nginx/html/index.html
cp dist/assets/*.js ~/scoop/persist/nginx/html/assets/ 2>/dev/null || true
cp dist/assets/*.css ~/scoop/persist/nginx/html/assets/ 2>/dev/null || true

echo "Verifying live site..."
if curl -sL http://zqmlabs.com/ | grep -q "div id=\"root\""; then
    echo "✓ Live site updated successfully"
else
    echo "✗ Verification failed — check nginx config"
fi
