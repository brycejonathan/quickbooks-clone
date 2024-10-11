"""
Main module for the Tax Service.

This module initializes the FastAPI app and defines the endpoints for tax calculations
and filings.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, utils
import logging
import psycopg2
import os

# Initialize FastAPI app
app = FastAPI(title="Tax Service", description="Tax calculations and compliance endpoints")

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

@app.post("/calculate_tax/", response_model=schemas.TaxCalculationResult)
def calculate_tax(tax_request: schemas.TaxCalculationRequest, db=Depends(get_db)):
    """
    Calculate tax based on provided income and deductions.

    Parameters:
    - tax_request: TaxCalculationRequest schema containing income and deductions.

    Returns:
    - TaxCalculationResult schema with calculated tax.
    """
    try:
        result = utils.calculate_tax(tax_request)
        return result
    except Exception as e:
        logger.exception("Error calculating tax")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/file_tax_return/", response_model=schemas.TaxFilingResult)
def file_tax_return(tax_filing: schemas.TaxFiling, db=Depends(get_db)):
    """
    File a tax return.

    Parameters:
    - tax_filing: TaxFiling schema containing tax return details.

    Returns:
    - TaxFilingResult schema indicating filing status.
    """
    try:
        result = utils.file_tax_return(tax_filing)
        return result
    except Exception as e:
        logger.exception("Error filing tax return")
        raise HTTPException(status_code=400, detail=str(e))
