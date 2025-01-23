import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "H3 API is running."}

def test_latlng_to_cell():
    response = client.get("/latlng_to_cell?lat=37&lng=-122&resolution=9")
    assert response.status_code == 200
    assert "cell" in response.json()
    assert response.json()["cell"] == "8928341aec3ffff"

def test_cell_to_latlng():
    cell = "8928341aec3ffff"
    response = client.get(f"/cell_to_latlng?cell={cell}")
    assert response.status_code == 200
    data = response.json()
    assert "lat" in data
    assert "lng" in data
    assert data["lat"] == 36.999615870313264
    assert data["lng"] == -121.99953914638627

def test_cell_to_boundary():
    cell = "8928341aec3ffff"
    response = client.get(f"/cell_to_boundary?cell={cell}")
    assert response.status_code == 200
    assert "boundary" in response.json()
    assert len(response.json()["boundary"]) == 6

def test_get_resolution():
    cell = "8928308280fffff"
    response = client.get(f"/get_resolution?cell={cell}")
    assert response.status_code == 200
    assert response.json() == {"resolution": 9}

def test_get_base_cell_number():
    cell = "8928308280fffff"
    response = client.get(f"/get_base_cell_number?cell={cell}")
    assert response.status_code == 200
    assert "base_cell_number" in response.json()

def test_str_to_int():
    cell = "8928308280fffff"
    response = client.get(f"/str_to_int?cell={cell}")
    assert response.status_code == 200
    assert "cell_int" in response.json()

def test_int_to_str():
    cell_int = 0x8928308280fffff
    response = client.get(f"/int_to_str?cell_int={cell_int}")
    assert response.status_code == 200
    assert "cell_str" in response.json()
    assert response.json()["cell_str"] == "8928308280fffff"
