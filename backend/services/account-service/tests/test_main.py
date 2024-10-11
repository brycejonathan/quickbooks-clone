"""
Test cases for the Account Service.
"""

from fastapi.testclient import TestClient
from app.main import app
import datetime

client = TestClient(app)

def test_create_invoice(monkeypatch):
    def mock_get_db():
        # Mock the database connection and cursor
        class MockCursor:
            def execute(self, sql, params):
                pass
            def fetchone(self):
                return [1]
            def close(self):
                pass
        class MockDB:
            def cursor(self):
                return MockCursor()
            def commit(self):
                pass
            def close(self):
                pass
        return MockDB()
    monkeypatch.setattr("app.main.get_db", mock_get_db)

    response = client.post("/invoices/", json={
        "customer_name": "Acme Corp",
        "amount": 1000.0,
        "due_date": datetime.date.today().isoformat()
    })
    assert response.status_code == 201
    assert response.json()["customer_name"] == "Acme Corp"

# Additional test cases would be implemented similarly
