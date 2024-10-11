"""
Main module for the Banking Service.

This module initializes the FastAPI app and defines the endpoints for managing bank accounts
and transactions, including reconciliation.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, crud, utils
import logging
import psycopg2
import os

# Initialize FastAPI app
app = FastAPI(title="Banking Service", description="Bank account and reconciliation endpoints")

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


# Bank Account Endpoints

@app.post("/bank_accounts/", response_model=schemas.BankAccount, status_code=status.HTTP_201_CREATED)
def create_bank_account(bank_account: schemas.BankAccountCreate, db=Depends(get_db)):
    """
    Create a new bank account.

    Parameters:
    - bank_account: BankAccountCreate schema containing bank account details.

    Returns:
    - BankAccount schema of the newly created bank account.
    """
    try:
        existing_account = crud.get_bank_account_by_number(db, bank_account.account_number)
        if existing_account:
            raise HTTPException(status_code=400, detail="Bank account already exists")
        return crud.create_bank_account(db, bank_account)
    except Exception as e:
        logger.exception("Error creating bank account")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/bank_accounts/{account_id}", response_model=schemas.BankAccount)
def read_bank_account(account_id: int, db=Depends(get_db)):
    """
    Retrieve a bank account by its ID.

    Parameters:
    - account_id: ID of the bank account.

    Returns:
    - BankAccount schema of the retrieved bank account.
    """
    account = crud.get_bank_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    return account


@app.post("/bank_transactions/", response_model=schemas.BankTransaction, status_code=status.HTTP_201_CREATED)
def create_bank_transaction(transaction: schemas.BankTransactionCreate, db=Depends(get_db)):
    """
    Create a new bank transaction.

    Parameters:
    - transaction: BankTransactionCreate schema containing transaction details.

    Returns:
    - BankTransaction schema of the newly created transaction.
    """
    try:
        return crud.create_bank_transaction(db, transaction)
    except Exception as e:
        logger.exception("Error creating bank transaction")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/reconcile/", status_code=status.HTTP_200_OK)
def reconcile_account(account_id: int, db=Depends(get_db)):
    """
    Reconcile a bank account.

    Parameters:
    - account_id: ID of the bank account to reconcile.

    Returns:
    - Reconciliation result.
    """
    try:
        result = utils.reconcile_bank_account(db, account_id)
        if not result:
            raise HTTPException(status_code=404, detail="Bank account not found or reconciliation failed")
        return {"message": "Bank account reconciled successfully"}
    except Exception as e:
        logger.exception("Error during reconciliation")
        raise HTTPException(status_code=400, detail=str(e))
