"""
Database models for the Inventory Service.

Defines SQL statements for creating the inventory_items table.
"""

inventory_item_table_creation = """
CREATE TABLE IF NOT EXISTS inventory_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    quantity INTEGER DEFAULT 0,
    price NUMERIC(12, 2) NOT NULL
);
"""
