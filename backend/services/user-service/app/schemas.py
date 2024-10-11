"""
Pydantic schemas for data validation and serialization.
"""

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    Base schema for User containing common fields.
    """
    email: EmailStr
    full_name: str = None


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str


class User(UserBase):
    """
    Schema representing a user.
    """
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    """
    Schema for JWT token.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for token data extracted from JWT.
    """
    email: EmailStr = None
