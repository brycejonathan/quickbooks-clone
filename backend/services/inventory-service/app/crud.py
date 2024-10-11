"""
CRUD operations for the Inventory Service using direct AWS RDS PostgreSQL connection.
"""

from . import schemas
import logging

logger = logging.getLogger(__name__)


def get_item(db, item_id: int):
    """
    Retrieve an item by ID.
    """
    cursor = db.cursor()
    sql = "SELECT id, name, description, quantity, price FROM inventory_items WHERE id = %s;"
    cursor.execute(sql, (item_id,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return schemas.InventoryItem(
            id=row[0],
            name=row[1],
            description=row[2],
            quantity=row[3],
            price=float(row[4])
        )
    return None


def get_item_by_name(db, name: str):
    """
    Retrieve an item by name.
    """
    cursor = db.cursor()
    sql = "SELECT id, name, description, quantity, price FROM inventory_items WHERE name = %s;"
    cursor.execute(sql, (name,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return schemas.InventoryItem(
            id=row[0],
            name=row[1],
            description=row[2],
            quantity=row[3],
            price=float(row[4])
        )
    return None


def create_item(db, item: schemas.InventoryItemCreate):
    """
    Create a new inventory item.
    """
    cursor = db.cursor()
    sql = """
        INSERT INTO inventory_items (name, description, quantity, price)
        VALUES (%s, %s, %s, %s) RETURNING id;
    """
    params = (item.name, item.description, item.quantity, item.price)
    cursor.execute(sql, params)
    item_id = cursor.fetchone()[0]
    db.commit()
    cursor.close()
    return get_item(db, item_id)


def update_item(db, item_id: int, item: schemas.InventoryItemUpdate):
    """
    Update an existing inventory item.
    """
    cursor = db.cursor()
    fields = []
    params = []
    if item.name is not None:
        fields.append("name = %s")
        params.append(item.name)
    if item.description is not None:
        fields.append("description = %s")
        params.append(item.description)
    if item.price is not None:
        fields.append("price = %s")
        params.append(item.price)
    if item.quantity is not None:
        fields.append("quantity = %s")
        params.append(item.quantity)
    params.append(item_id)
    sql = f"UPDATE inventory_items SET {', '.join(fields)} WHERE id = %s;"
    cursor.execute(sql, params)
    db.commit()
    cursor.close()
    return get_item(db, item_id)


def delete_item(db, item_id: int):
    """
    Delete an inventory item.
    """
    cursor = db.cursor()
    sql = "DELETE FROM inventory_items WHERE id = %s;"
    cursor.execute(sql, (item_id,))
    db.commit()
    cursor.close()
    return cursor.rowcount > 0
