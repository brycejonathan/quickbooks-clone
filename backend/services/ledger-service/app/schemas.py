"""
Pydantic schemas for data validation and serialization.
"""

from pydantic import BaseModel


class AccountBase(BaseModel):
    """
    Base schema for Account containing common fields.
    """
    name: str
    type: str


class AccountCreate(AccountBase):
    """
    Schema for creating a new account.
    """
    balance: float = 0.0


class AccountUpdate(BaseModel):
    """
    Schema for updating an existing account.
    """
    name: str = None
    type: str = None
    balance: float = None


class Account(AccountBase):
    """
    Schema representing an account.
    """
    id: int
    balance: float

    class Config:
        orm_mode = True
