"""
Utility functions for the Reporting Service.
"""

import time
from .database import get_connection
from .crud import update_report_status
import logging

logger = logging.getLogger(__name__)

def generate_report(report_id: int):
    """
    Generate the report and update the status.

    Parameters:
    - report_id: ID of the report to generate.
    """
    db = get_connection()
    try:
        # Simulate report generation
        logger.info(f"Starting report generation for report ID: {report_id}")
        time.sleep(5)  # Simulate time-consuming task
        file_path = f"/reports/report_{report_id}.pdf"  # Placeholder for actual report file
        # Update report status to 'Completed'
        update_report_status(db, report_id, status="Completed", file_path=file_path)
        logger.info(f"Report generation completed for report ID: {report_id}")
    except Exception as e:
        logger.exception("Error generating report")
        update_report_status(db, report_id, status="Failed")
    finally:
        db.close()
