"""
Database models for the Audit Service.

Defines SQL statements for creating the audit_logs table.
"""

audit_logs_table_creation = """
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    action VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'),
    details TEXT
);
"""
