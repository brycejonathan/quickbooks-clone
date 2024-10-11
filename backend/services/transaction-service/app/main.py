"""
Main module for the Transaction Service.

This module initializes the FastAPI app and defines the endpoints for managing financial transactions.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, crud, database, utils
import logging

# Initialize FastAPI app
app = FastAPI(title="Transaction Service", description="Financial transaction management endpoints")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db():
    """
    Dependency to get a database connection.
    """
    db = database.get_connection()
    try:
        yield db
    finally:
        db.close()


@app.post("/transactions/", response_model=schemas.Transaction, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: schemas.TransactionCreate, db=Depends(get_db)):
    """
    Create a new financial transaction.

    Parameters:
    - transaction: TransactionCreate schema containing transaction details.

    Returns:
    - Transaction schema of the newly created transaction.
    """
    try:
        result = crud.create_transaction(db, transaction)
        return result
    except Exception as e:
        logger.exception("Error creating transaction")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/transactions/{transaction_id}", response_model=schemas.Transaction)
def read_transaction(transaction_id: int, db=Depends(get_db)):
    """
    Retrieve a transaction by its ID.

    Parameters:
    - transaction_id: ID of the transaction.

    Returns:
    - Transaction schema of the retrieved transaction.
    """
    transaction = crud.get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@app.put("/transactions/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(transaction_id: int, transaction: schemas.TransactionUpdate, db=Depends(get_db)):
    """
    Update an existing transaction.

    Parameters:
    - transaction_id: ID of the transaction to update.
    - transaction: TransactionUpdate schema containing updated fields.

    Returns:
    - Transaction schema of the updated transaction.
    """
    try:
        updated_transaction = crud.update_transaction(db, transaction_id, transaction)
        if not updated_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return updated_transaction
    except Exception as e:
        logger.exception("Error updating transaction")
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db=Depends(get_db)):
    """
    Delete a transaction by its ID.

    Parameters:
    - transaction_id: ID of the transaction to delete.
    """
    try:
        result = crud.delete_transaction(db, transaction_id)
        if not result:
            raise HTTPException(status_code=404, detail="Transaction not found")
    except Exception as e:
        logger.exception("Error deleting transaction")
        raise HTTPException(status_code=400, detail=str(e))
