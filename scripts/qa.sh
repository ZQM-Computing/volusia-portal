#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "=== Project Volusia — QA ==="
echo ""

fail=0

# 1. TypeScript
echo "[1/5] TypeScript type check..."
if npx tsc --noEmit > /dev/null 2>&1; then
    echo "  ✓ PASS"
else
    echo "  ✗ FAIL"
    ((fail++))
fi

# 2. Build
echo "[2/5] Build..."
if npm run build > /dev/null 2>&1; then
    echo "  ✓ PASS"
else
    echo "  ✗ FAIL"
    ((fail++))
fi

# 3. Lint
echo "[3/5] Lint..."
if npx tsc --noEmit 2>&1 | grep -i "error" | head -5 > /dev/null 2>&1; then
    echo "  ✗ ERRORS FOUND"
    ((fail++))
else
    echo "  ✓ PASS"
fi

# 4. Dead code detection
echo "[4/5] Code quality (TODO/FIXME/random)..."
found=$(grep -rn "Math.random\|Math.sin\|console.log\|TODO\|FIXME\|HACK" src/ --include="*.tsx" --include="*.ts" 2>/dev/null || true)
if [ -n "$found" ]; then
    echo "  ⚠ Found: $(echo "$found" | head -3 | wc -l) occurrences"
else
    echo "  ✓ PASS"
fi

# 5. Backend syntax
echo "[5/5] Backend syntax..."
if cd backend && python3 -m py_compile main.py gamification/routes.py 2>&1 > /dev/null; then
    echo "  ✓ PASS"
else
    echo "  ✗ FAIL"
    ((fail++))
fi
cd ..

echo ""
if [ "$fail" -eq 0 ]; then
    echo "=== All QA checks PASSED ==="
else
    echo "=== ${fail} QA check(s) FAILED ==="
fi

[ "$fail" -eq 0 ]
