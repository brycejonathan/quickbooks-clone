"""
Test cases for the Tax Service.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_calculate_tax():
    response = client.post("/calculate_tax/", json={
        "income": 60000,
        "deductions": 10000
    })
    assert response.status_code == 200
    result = response.json()
    assert result["taxable_income"] == 50000
    assert result["tax_due"] > 0


def test_file_tax_return():
    response = client.post("/file_tax_return/", json={
        "user_id": 1,
        "filing_year": 2021,
        "income": 60000,
        "deductions": 10000
    })
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "Filed"
    assert result["filing_id"] == 12345
