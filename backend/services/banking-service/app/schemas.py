"""
Pydantic schemas for data validation and serialization.
"""

from pydantic import BaseModel
import datetime


# Bank Account Schemas

class BankAccountBase(BaseModel):
    """
    Base schema for BankAccount containing common fields.
    """
    account_name: str
    account_number: str


class BankAccountCreate(BankAccountBase):
    """
    Schema for creating a new bank account.
    """
    balance: float = 0.0


class BankAccount(BankAccountBase):
    """
    Schema representing a bank account.
    """
    id: int
    balance: float

    class Config:
        orm_mode = True


# Bank Transaction Schemas

class BankTransactionBase(BaseModel):
    """
    Base schema for BankTransaction containing common fields.
    """
    bank_account_id: int
    description: str
    amount: float
    transaction_type: str  # 'Debit' or 'Credit'


class BankTransactionCreate(BankTransactionBase):
    """
    Schema for creating a new bank transaction.
    """
    pass


class BankTransaction(BankTransactionBase):
    """
    Schema representing a bank transaction.
    """
    id: int
    date: datetime.datetime

    class Config:
        orm_mode = True
