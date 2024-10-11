"""
Test cases for the Data Quality Service.
"""

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_validate_data():
    response = client.post("/validate_data/", json={
        "field_name": "email",
        "value": "invalid_email"
    })
    assert response.status_code == 200
    result = response.json()
    assert not result["is_valid"]
    assert "Invalid email format." in result["errors"]


def test_data_quality_report(monkeypatch):
    def mock_get_db():
        class MockCursor:
            def execute(self, sql):
                pass

            def fetchall(self):
                return [
                    (1, "Missing Data", "Email is missing", "2021-01-01T00:00:00", False),
                    (2, "Invalid Format", "Invalid email format", "2021-01-02T00:00:00", True)
                ]

            def close(self):
                pass

        class MockDB:
            def cursor(self):
                return MockCursor()

            def close(self):
                pass

        return MockDB()

    monkeypatch.setattr("app.main.get_db", mock_get_db)
    response = client.get("/data_quality_report/")
    assert response.status_code == 200
    report = response.json()
    assert report["total_issues"] == 2
    assert report["unresolved_issues"] == 1
