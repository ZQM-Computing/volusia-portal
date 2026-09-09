#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# Install dev dependencies
echo "Installing dev dependencies..."
npm install -D concurrently prettier eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin 2>/dev/null && echo "✓ Dev deps installed" || echo "⚠ Some deps may have failed"

# Install backend deps
cd backend && pip install -r requirements.txt 2>/dev/null && echo "✓ Backend deps installed" || echo "⚠ Backend deps may already be installed"
cd ..

# Create .env from .env.example if missing
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env from .env.example — EDIT IT WITH YOUR API KEYS"
else
    echo "✓ .env already exists"
fi

echo ""
echo "=== Dev environment ready! ==="
echo "  npm run dev        # Start frontend"
echo "  bash scripts/dev.sh # Start all services"
echo "  bash scripts/qa.sh   # Run quality checks"
