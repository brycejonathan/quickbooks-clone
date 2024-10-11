"""
Main module for the Accounting Service.

This module initializes the FastAPI app and defines the endpoints for managing financial statements,
such as balance sheets and income statements.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, crud, utils
import logging
import psycopg2
import os

# Initialize FastAPI app
app = FastAPI(title="Accounting Service", description="Financial statements management endpoints")

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


@app.get("/financial_statements/balance_sheet/", response_model=schemas.BalanceSheet)
def get_balance_sheet(db=Depends(get_db)):
    """
    Retrieve the balance sheet.

    Returns:
    - BalanceSheet schema containing assets, liabilities, and equity.
    """
    try:
        balance_sheet = crud.generate_balance_sheet(db)
        return balance_sheet
    except Exception as e:
        logger.exception("Error generating balance sheet")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/financial_statements/income_statement/", response_model=schemas.IncomeStatement)
def get_income_statement(db=Depends(get_db)):
    """
    Retrieve the income statement.

    Returns:
    - IncomeStatement schema containing revenues and expenses.
    """
    try:
        income_statement = crud.generate_income_statement(db)
        return income_statement
    except Exception as e:
        logger.exception("Error generating income statement")
        raise HTTPException(status_code=400, detail=str(e))
