"""
Main module for the Reporting Service.

This module initializes the FastAPI app and defines the endpoints for generating financial reports.
"""

from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from . import schemas, crud, utils, database
import logging

# Initialize FastAPI app
app = FastAPI(title="Reporting Service", description="Financial reporting endpoints")

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

@app.post("/reports/", response_model=schemas.Report, status_code=status.HTTP_202_ACCEPTED)
def generate_report(report_request: schemas.ReportCreate, background_tasks: BackgroundTasks, db=Depends(get_db)):
    """
    Generate a financial report asynchronously.

    Parameters:
    - report_request: ReportCreate schema containing report details.

    Returns:
    - Report schema indicating the report generation has started.
    """
    try:
        report = crud.create_report(db, report_request)
        background_tasks.add_task(utils.generate_report, report.id)
        return report
    except Exception as e:
        logger.exception("Error generating report")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/reports/{report_id}", response_model=schemas.Report)
def get_report(report_id: int, db=Depends(get_db)):
    """
    Retrieve a report by its ID.

    Parameters:
    - report_id: ID of the report.

    Returns:
    - Report schema of the retrieved report.
    """
    report = crud.get_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
