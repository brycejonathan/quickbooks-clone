"""
Pydantic schemas for data validation and serialization.
"""

from pydantic import BaseModel


class IntegrationBase(BaseModel):
    """
    Base schema for Integration containing common fields.
    """
    name: str
    endpoint_url: str


class IntegrationCreate(IntegrationBase):
    """
    Schema for creating a new integration.
    """
    api_key: str
    api_secret: str


class Integration(IntegrationBase):
    """
    Schema representing an integration.
    """
    id: int
    last_synced: str = None

    class Config:
        orm_mode = True
