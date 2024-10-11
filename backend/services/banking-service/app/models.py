"""
Database models for the Banking Service.

Defines SQL statements for creating the bank_accounts and bank_transactions tables.
"""

bank_account_table_creation = """
CREATE TABLE IF NOT EXISTS bank_accounts (
    id SERIAL PRIMARY KEY,
    account_name VARCHAR(255) NOT NULL,
    account_number VARCHAR(50) UNIQUE NOT NULL,
    balance NUMERIC(12, 2) DEFAULT 0.0
);
"""

bank_transaction_table_creation = """
CREATE TABLE IF NOT EXISTS bank_transactions (
    id SERIAL PRIMARY KEY,
    bank_account_id INTEGER NOT NULL REFERENCES bank_accounts(id),
    description TEXT NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    date TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'),
    transaction_type VARCHAR(10) NOT NULL  -- 'Debit' or 'Credit'
);
"""
