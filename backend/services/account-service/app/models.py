"""
Database models for the Accounting Service.

Defines SQL statements for creating the accounts and transactions tables.
"""

accounts_table_creation = """
CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL,
    balance NUMERIC(12, 2) DEFAULT 0.0
);
"""

transactions_table_creation = """
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    description TEXT,
    amount NUMERIC(12, 2) NOT NULL,
    date TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'),
    transaction_type VARCHAR(10) NOT NULL  -- 'Debit' or 'Credit'
);
"""
