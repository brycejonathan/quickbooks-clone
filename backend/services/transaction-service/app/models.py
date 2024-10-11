"""
Database models for the Transaction Service.
"""

# Since we're using direct SQL queries, models.py may not be necessary.
# However, for clarity, we can define table creation SQL statements here.

transaction_table_creation = """
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    date TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'),
    account_id INTEGER NOT NULL,
    transaction_type VARCHAR(10) NOT NULL  -- 'Debit' or 'Credit'
);
"""
