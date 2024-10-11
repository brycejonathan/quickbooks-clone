"""
Database models for the Tax Service.

Defines SQL statements for creating the tax_filings table.
"""

tax_filings_table_creation = """
CREATE TABLE IF NOT EXISTS tax_filings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    filing_year INTEGER NOT NULL,
    income NUMERIC(12, 2) NOT NULL,
    deductions NUMERIC(12, 2) NOT NULL,
    tax_due NUMERIC(12, 2) NOT NULL,
    filed_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'),
    status VARCHAR(50) DEFAULT 'Pending'
);
"""
