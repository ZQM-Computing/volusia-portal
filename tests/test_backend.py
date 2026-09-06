"""Project Volusia — Backend tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

import pytest

def test_import_main():
    import main
    assert main.app is not None
    assert main.app.title == "Project Volusia API"

def test_app_health():
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["indicator_count"] > 0

def test_app_indicators():
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)
    response = client.get("/indicators")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] > 0
    assert "indicators" in data

def test_app_map_layers():
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)
    response = client.get("/map-layers")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 18
    assert "layers" in data

def test_app_datasets():
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)
    response = client.get("/datasets")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 10
    assert "datasets" in data

def test_app_indicator_by_name():
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)
    response = client.get("/indicators/median_household_income_acs")
    assert response.status_code == 200

def test_app_diagnostics():
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)
    response = client.get("/diagnostics")
    assert response.status_code == 200
    data = response.json()
    assert data["overall"] == "healthy"
    assert data["checks"]["database"] is True
    assert data["checks"]["api_endpoints"] is True
    assert data["checks"]["map_layers"] is True
