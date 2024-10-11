"""
Main module for the Ledger Service.

This module initializes the FastAPI app and defines the endpoints for managing accounts
and the general ledger.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, crud, utils
import logging
import psycopg2
import os

# Initialize FastAPI app
app = FastAPI(title="Ledger Service", description="Ledger management endpoints")

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


@app.post("/accounts/", response_model=schemas.Account, status_code=status.HTTP_201_CREATED)
def create_account(account: schemas.AccountCreate, db=Depends(get_db)):
    """
    Create a new account in the ledger.

    Parameters:
    - account: AccountCreate schema containing account details.

    Returns:
    - Account schema of the newly created account.
    """
    try:
        existing_account = crud.get_account_by_name(db, account.name)
        if existing_account:
            raise HTTPException(status_code=400, detail="Account already exists")
        return crud.create_account(db, account)
    except Exception as e:
        logger.exception("Error creating account")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/accounts/{account_id}", response_model=schemas.Account)
def read_account(account_id: int, db=Depends(get_db)):
    """
    Retrieve an account by its ID.

    Parameters:
    - account_id: ID of the account.

    Returns:
    - Account schema of the retrieved account.
    """
    account = crud.get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@app.put("/accounts/{account_id}", response_model=schemas.Account)
def update_account(account_id: int, account: schemas.AccountUpdate, db=Depends(get_db)):
    """
    Update an existing account.

    Parameters:
    - account_id: ID of the account to update.
    - account: AccountUpdate schema containing updated fields.

    Returns:
    - Account schema of the updated account.
    """
    try:
        updated_account = crud.update_account(db, account_id, account)
        if not updated_account:
            raise HTTPException(status_code=404, detail="Account not found")
        return updated_account
    except Exception as e:
        logger.exception("Error updating account")
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, db=Depends(get_db)):
    """
    Delete an account by its ID.

    Parameters:
    - account_id: ID of the account to delete.
    """
    try:
        result = crud.delete_account(db, account_id)
        if not result:
            raise HTTPException(status_code=404, detail="Account not found")
    except Exception as e:
        logger.exception("Error deleting account")
        raise HTTPException(status_code=400, detail=str(e))
