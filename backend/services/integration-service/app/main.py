"""
Main module for the Integration Service.

This module initializes the FastAPI app and defines the endpoints for managing integrations
with external services and APIs.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, crud, utils
import logging
import psycopg2
import os

# Initialize FastAPI app
app = FastAPI(title="Integration Service", description="External integrations management endpoints")

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

@app.post("/integrations/", response_model=schemas.Integration, status_code=status.HTTP_201_CREATED)
def create_integration(integration: schemas.IntegrationCreate, db=Depends(get_db)):
    """
    Create a new integration.

    Parameters:
    - integration: IntegrationCreate schema containing integration details.

    Returns:
    - Integration schema of the newly created integration.
    """
    try:
        existing_integration = crud.get_integration_by_name(db, integration.name)
        if existing_integration:
            raise HTTPException(status_code=400, detail="Integration already exists")
        return crud.create_integration(db, integration)
    except Exception as e:
        logger.exception("Error creating integration")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/integrations/{integration_id}", response_model=schemas.Integration)
def read_integration(integration_id: int, db=Depends(get_db)):
    """
    Retrieve an integration by ID.

    Parameters:
    - integration_id: ID of the integration.

    Returns:
    - Integration schema of the retrieved integration.
    """
    integration = crud.get_integration(db, integration_id)
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    return integration

@app.post("/integrations/{integration_id}/sync/", status_code=status.HTTP_200_OK)
def sync_integration(integration_id: int, db=Depends(get_db)):
    """
    Trigger synchronization for an integration.

    Parameters:
    - integration_id: ID of the integration to synchronize.

    Returns:
    - Synchronization result.
    """
    try:
        integration = crud.get_integration(db, integration_id)
        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")
        utils.sync_integration_data(integration)
        return {"message": f"Integration '{integration.name}' synchronized successfully"}
    except Exception as e:
        logger.exception("Error synchronizing integration")
        raise HTTPException(status_code=400, detail=str(e))
