"""
CRUD operations for the Integration Service using direct AWS RDS PostgreSQL connection.
"""

from . import schemas
import logging

logger = logging.getLogger(__name__)


def get_integration(db, integration_id: int):
    """
    Retrieve an integration by ID.
    """
    cursor = db.cursor()
    sql = """
        SELECT id, name, endpoint_url, last_synced
        FROM integrations WHERE id = %s;
    """
    cursor.execute(sql, (integration_id,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return schemas.Integration(
            id=row[0],
            name=row[1],
            endpoint_url=row[2],
            last_synced=row[3]
        )
    return None


def get_integration_by_name(db, name: str):
    """
    Retrieve an integration by name.
    """
    cursor = db.cursor()
    sql = """
        SELECT id, name, endpoint_url, last_synced
        FROM integrations WHERE name = %s;
    """
    cursor.execute(sql, (name,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return schemas.Integration(
            id=row[0],
            name=row[1],
            endpoint_url=row[2],
            last_synced=row[3]
        )
    return None


def create_integration(db, integration: schemas.IntegrationCreate):
    """
    Create a new integration.
    """
    cursor = db.cursor()
    sql = """
        INSERT INTO integrations (name, api_key, api_secret, endpoint_url)
        VALUES (%s, %s, %s, %s) RETURNING id;
    """
    params = (integration.name, integration.api_key, integration.api_secret, integration.endpoint_url)
    cursor.execute(sql, params)
    integration_id = cursor.fetchone()[0]
    db.commit()
    cursor.close()
    return get_integration(db, integration_id)
