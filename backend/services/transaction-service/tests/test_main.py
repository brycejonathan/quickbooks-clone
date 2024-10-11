"""
Test cases for the Transaction Service.
"""

from fastapi.testclient import TestClient
from app.main import app
import datetime
import pytest

client = TestClient(app)

@pytest.fixture
def mock_db(monkeypatch):
    class MockCursor:
        def execute(self, sql, params=None):
            pass
        def fetchone(self):
            return [1, "Test Transaction", 100.0, datetime.datetime.utcnow(), 1, "Debit"]
        def close(self):
            pass
    class MockDB:
        def cursor(self):
            return MockCursor()
        def commit(self):
            pass
        def close(self):
            pass
    monkeypatch.setattr("app.main.get_db", lambda: MockDB())

def test_create_transaction(mock_db):
    response = client.post("/transactions/", json={
        "description": "Test Transaction",
        "amount": 100.0,
        "account_id": 1,
        "transaction_type": "Debit"
    })
    assert response.status_code == 201
    assert response.json()["description"] == "Test Transaction"
