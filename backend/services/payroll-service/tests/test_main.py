"""
Test cases for the Payroll Service.
"""

from fastapi.testclient import TestClient
from app.main import app
import pytest
import datetime

client = TestClient(app)


@pytest.fixture
def mock_db(monkeypatch):
    class MockCursor:
        def execute(self, sql, params=None):
            pass

        def fetchone(self):
            return [1, "John Doe", "john@example.com", "Developer", 60000.0, datetime.date.today()]

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


def test_create_employee(mock_db):
    response = client.post("/employees/", json={
        "full_name": "John Doe",
        "email": "john@example.com",
        "position": "Developer",
        "salary": 60000.0,
        "date_hired": datetime.date.today().isoformat()
    })
    assert response.status_code == 201
    assert response.json()["full_name"] == "John Doe"
