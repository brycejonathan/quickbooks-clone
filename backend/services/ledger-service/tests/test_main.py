"""
Test cases for the Ledger Service.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_account():
    response = client.post("/accounts/", json={
        "name": "Cash",
        "type": "Asset",
        "balance": 1000.0
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Cash"

def test_read_account():
    response = client.get("/accounts/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Cash"

def test_update_account():
    response = client.put("/accounts/1", json={
        "balance": 1500.0
    })
    assert response.status_code == 200
    assert response.json()["balance"] == 1500.0

def test_delete_account():
    response = client.delete("/accounts/1")
    assert response.status_code == 204
