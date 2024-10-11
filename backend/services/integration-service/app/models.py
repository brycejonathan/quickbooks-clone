"""
Database models for the Integration Service.

Defines SQL statements for creating the integrations table.
"""

integrations_table_creation = """
CREATE TABLE IF NOT EXISTS integrations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    api_key VARCHAR(255) NOT NULL,
    api_secret VARCHAR(255) NOT NULL,
    endpoint_url TEXT NOT NULL,
    last_synced TIMESTAMP WITHOUT TIME ZONE
);
"""
