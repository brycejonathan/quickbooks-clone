"""
Database models for the Data Quality Service.

Defines SQL statements for creating the data_quality_issues table.
"""

data_quality_issues_table_creation = """
CREATE TABLE IF NOT EXISTS data_quality_issues (
    id SERIAL PRIMARY KEY,
    issue_type VARCHAR(255) NOT NULL,
    description TEXT,
    detected_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'),
    resolved BOOLEAN DEFAULT FALSE
);
"""
