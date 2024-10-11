"""
Main module for the Inventory Service.

This module initializes the FastAPI app and defines the endpoints for managing inventory items and stock levels.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, crud, utils
import logging
import psycopg2
import os

# Initialize FastAPI app
app = FastAPI(title="Inventory Service", description="Inventory management endpoints")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    """
    Dependency to get a database connection.
    """
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT", 5432)),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD")
    )
    try:
        yield conn
    finally:
        conn.close()

@app.post("/items/", response_model=schemas.InventoryItem, status_code=status.HTTP_201_CREATED)
def create_item(item: schemas.InventoryItemCreate, db=Depends(get_db)):
    """
    Create a new inventory item.

    Parameters:
    - item: InventoryItemCreate schema containing item details.

    Returns:
    - InventoryItem schema of the newly created item.
    """
    try:
        existing_item = crud.get_item_by_name(db, item.name)
        if existing_item:
            raise HTTPException(status_code=400, detail="Item already exists")
        return crud.create_item(db, item)
    except Exception as e:
        logger.exception("Error creating item")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/items/{item_id}", response_model=schemas.InventoryItem)
def read_item(item_id: int, db=Depends(get_db)):
    """
    Retrieve an item by its ID.

    Parameters:
    - item_id: ID of the item.

    Returns:
    - InventoryItem schema of the retrieved item.
    """
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=schemas.InventoryItem)
def update_item(item_id: int, item: schemas.InventoryItemUpdate, db=Depends(get_db)):
    """
    Update an existing inventory item.

    Parameters:
    - item_id: ID of the item to update.
    - item: InventoryItemUpdate schema containing updated fields.

    Returns:
    - InventoryItem schema of the updated item.
    """
    try:
        updated_item = crud.update_item(db, item_id, item)
        if not updated_item:
            raise HTTPException(status_code=404, detail="Item not found")
        return updated_item
    except Exception as e:
        logger.exception("Error updating item")
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db=Depends(get_db)):
    """
    Delete an item by its ID.

    Parameters:
    - item_id: ID of the item to delete.
    """
    try:
        result = crud.delete_item(db, item_id)
        if not result:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        logger.exception("Error deleting item")
        raise HTTPException(status_code=400, detail=str(e))
