"""
Main module for the Audit Service.

This module initializes the FastAPI app and defines the endpoints for managing audit logs
and conducting audits.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, crud
import logging
import psycopg2
import os

# Initialize FastAPI app
app = FastAPI(title="Audit Service", description="Audit logging and management endpoints")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    """
    Dependency to get a database connection.
    """
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT", 5432)),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD")
    )
    try:
        yield conn
    finally:
        conn.close()

@app.post("/audit_logs/", response_model=schemas.AuditLog, status_code=status.HTTP_201_CREATED)
def create_audit_log(audit_log: schemas.AuditLogCreate, db=Depends(get_db)):
    """
    Create a new audit log entry.

    Parameters:
    - audit_log: AuditLogCreate schema containing audit log details.

    Returns:
    - AuditLog schema of the newly created audit log.
    """
    try:
        result = crud.create_audit_log(db, audit_log)
        return result
    except Exception as e:
        logger.exception("Error creating audit log")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/audit_logs/{log_id}", response_model=schemas.AuditLog)
def read_audit_log(log_id: int, db=Depends(get_db)):
    """
    Retrieve an audit log entry by ID.

    Parameters:
    - log_id: ID of the audit log.

    Returns:
    - AuditLog schema of the retrieved audit log.
    """
    audit_log = crud.get_audit_log(db, log_id)
    if not audit_log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return audit_log

@app.get("/audit_logs/", response_model=schemas.AuditLogList)
def list_audit_logs(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    """
    Retrieve a list of audit logs.

    Parameters:
    - skip: Number of records to skip.
    - limit: Maximum number of records to return.

    Returns:
    - List of AuditLog schemas.
    """
    audit_logs = crud.get_audit_logs(db, skip, limit)
    return schemas.AuditLogList(audit_logs=audit_logs)
