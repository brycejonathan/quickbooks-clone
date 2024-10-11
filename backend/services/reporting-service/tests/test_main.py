"""
Test cases for the Reporting Service.
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
            return [1, "balance_sheet", "Pending", None, None, None]

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


def test_generate_report(mock_db):
    response = client.post("/reports/", json={
        "report_type": "balance_sheet"
    })
    assert response.status_code == 202
    assert response.json()["report_type"] == "balance_sheet"
    assert response.json()["status"] == "Pending"
