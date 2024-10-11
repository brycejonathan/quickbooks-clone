"""
Database connection management using AWS RDS PostgreSQL.
"""

import psycopg2
import os

def get_connection():
    """
    Establishes a connection to the AWS RDS PostgreSQL database.

    Returns:
    - A database connection object.
    """
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT", 5432)),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD")
    )
    return conn
