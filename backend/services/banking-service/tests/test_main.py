"""
Test cases for the Banking Service.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_bank_account():
    response = client.post("/bank_accounts/", json={
        "account_name": "Business Checking",
        "account_number": "123456789",
        "balance": 5000.0
    })
    assert response.status_code == 201
    assert response.json()["account_name"] == "Business Checking"

def test_create_bank_transaction():
    response = client.post("/bank_transactions/", json={
        "bank_account_id": 1,
        "description": "Deposit",
        "amount": 1000.0,
        "transaction_type": "Credit"
    })
    assert response.status_code == 201
    assert response.json()["description"] == "Deposit"

def test_reconcile_account():
    response = client.post("/reconcile/", params={"account_id": 1})
    assert response.status_code == 200
    assert response.json()["message"] == "Bank account reconciled successfully"
