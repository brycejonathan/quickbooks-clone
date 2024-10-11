"""
Main module for the Data Quality Service.

This module initializes the FastAPI app and defines the endpoints for data validation
and quality checks.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, utils
import logging
import psycopg2
import os

# Initialize FastAPI app
app = FastAPI(title="Data Quality Service", description="Data validation and quality checks endpoints")

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

@app.post("/validate_data/", response_model=schemas.ValidationResult)
def validate_data(data: schemas.DataInput, db=Depends(get_db)):
    """
    Validate input data against predefined rules.

    Parameters:
    - data: DataInput schema containing data to be validated.

    Returns:
    - ValidationResult schema indicating the validation outcome.
    """
    try:
        result = utils.validate_data(data)
        return result
    except Exception as e:
        logger.exception("Error validating data")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/data_quality_report/", response_model=schemas.DataQualityReport)
def data_quality_report(db=Depends(get_db)):
    """
    Generate a data quality report.

    Returns:
    - DataQualityReport schema containing data quality metrics.
    """
    try:
        report = utils.generate_data_quality_report(db)
        return report
    except Exception as e:
        logger.exception("Error generating data quality report")
        raise HTTPException(status_code=400, detail=str(e))
