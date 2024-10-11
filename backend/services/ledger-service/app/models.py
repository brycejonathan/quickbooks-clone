"""
Database models for the Ledger Service.

Defines SQL statements for creating the accounts table.
"""

account_table_creation = """
CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL,
    balance NUMERIC(12, 2) DEFAULT 0.0
);
"""
