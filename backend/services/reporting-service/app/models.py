"""
Database models for the Reporting Service.

Defines SQL statements for creating the reports table.
"""

report_table_creation = """
CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    report_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'),
    completed_at TIMESTAMP WITHOUT TIME ZONE,
    file_path TEXT
);
"""
