"""
Pydantic schemas for data validation and serialization.
"""

from pydantic import BaseModel


class InventoryItemBase(BaseModel):
    """
    Base schema for InventoryItem containing common fields.
    """
    name: str
    description: str = None
    price: float


class InventoryItemCreate(InventoryItemBase):
    """
    Schema for creating a new inventory item.
    """
    quantity: int = 0


class InventoryItemUpdate(BaseModel):
    """
    Schema for updating an existing inventory item.
    """
    name: str = None
    description: str = None
    price: float = None
    quantity: int = None


class InventoryItem(InventoryItemBase):
    """
    Schema representing an inventory item.
    """
    id: int
    quantity: int

    class Config:
        orm_mode = True
