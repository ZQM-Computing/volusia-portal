import sys, os
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
# Ensure VOLUSIA_REFRESH_TOKEN is set for tests
os.environ.setdefault("VOLUSIA_REFRESH_TOKEN", "volusia-refresh-secret-2026-secure")
