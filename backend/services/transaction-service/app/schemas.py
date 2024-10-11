"""
Pydantic schemas for data validation and serialization.
"""

from pydantic import BaseModel
import datetime

class TransactionBase(BaseModel):
    """
    Base schema for Transaction containing common fields.
    """
    description: str
    amount: float
    account_id: int
    transaction_type: str  # 'Debit' or 'Credit'

class TransactionCreate(TransactionBase):
    """
    Schema for creating a new transaction.
    """
    pass

class TransactionUpdate(BaseModel):
    """
    Schema for updating an existing transaction.
    """
    description: str = None
    amount: float = None
    account_id: int = None
    transaction_type: str = None

class Transaction(TransactionBase):
    """
    Schema representing a transaction.
    """
    id: int
    date: datetime.datetime

    class Config:
        orm_mode = True
