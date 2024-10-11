"""
Pydantic schemas for data validation and serialization.
"""

from pydantic import BaseModel
from typing import List


class Account(BaseModel):
    """
    Schema representing an account.
    """
    id: int
    name: str
    type: str
    balance: float

    class Config:
        orm_mode = True


class Transaction(BaseModel):
    """
    Schema representing a transaction.
    """
    id: int
    account_id: int
    description: str
    amount: float
    date: str
    transaction_type: str

    class Config:
        orm_mode = True


class BalanceSheet(BaseModel):
    """
    Schema representing a balance sheet.
    """
    assets: float
    liabilities: float
    equity: float


class IncomeStatement(BaseModel):
    """
    Schema representing an income statement.
    """
    revenues: float
    expenses: float
    net_income: float
