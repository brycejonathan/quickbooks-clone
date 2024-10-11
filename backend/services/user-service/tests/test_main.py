"""
Test cases for the User Service.
"""

from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)


@pytest.fixture
def mock_db(monkeypatch):
    class MockCursor:
        def execute(self, sql, params=None):
            pass

        def fetchone(self):
            return [1, "test@example.com", "Test User", True, False]

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


def test_register_user(mock_db):
    response = client.post("/register", json={
        "email": "test@example.com",
        "password": "testpass",
        "full_name": "Test User"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
