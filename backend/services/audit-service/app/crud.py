"""
CRUD operations for the Audit Service using direct AWS RDS PostgreSQL connection.
"""

from . import schemas
import logging

logger = logging.getLogger(__name__)


def create_audit_log(db, audit_log: schemas.AuditLogCreate):
    """
    Create a new audit log entry.
    """
    cursor = db.cursor()
    sql = """
        INSERT INTO audit_logs (user_id, action, timestamp, details)
        VALUES (%s, %s, %s, %s) RETURNING id;
    """
    params = (
        audit_log.user_id,
        audit_log.action,
        None,  # Timestamp defaults to current time
        audit_log.details
    )
    cursor.execute(sql, params)
    log_id = cursor.fetchone()[0]
    db.commit()
    cursor.close()
    return get_audit_log(db, log_id)


def get_audit_log(db, log_id: int):
    """
    Retrieve an audit log entry by ID.
    """
    cursor = db.cursor()
    sql = """
        SELECT id, user_id, action, timestamp, details
        FROM audit_logs WHERE id = %s;
    """
    cursor.execute(sql, (log_id,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return schemas.AuditLog(
            id=row[0],
            user_id=row[1],
            action=row[2],
            timestamp=row[3],
            details=row[4]
        )
    return None


def get_audit_logs(db, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of audit logs.
    """
    cursor = db.cursor()
    sql = """
        SELECT id, user_id, action, timestamp, details
        FROM audit_logs ORDER BY timestamp DESC OFFSET %s LIMIT %s;
    """
    cursor.execute(sql, (skip, limit))
    rows = cursor.fetchall()
    cursor.close()
    audit_logs = [
        schemas.AuditLog(
            id=row[0],
            user_id=row[1],
            action=row[2],
            timestamp=row[3],
            details=row[4]
        ) for row in rows
    ]
    return audit_logs
