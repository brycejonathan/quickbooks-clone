"""
CRUD operations for the Reporting Service using direct AWS RDS PostgreSQL connection.
"""

from . import schemas
import datetime
import logging

logger = logging.getLogger(__name__)


def create_report(db, report_request: schemas.ReportCreate):
    """
    Create a new report request.

    Parameters:
    - db: Database connection.
    - report_request: ReportCreate schema.

    Returns:
    - Report schema.
    """
    cursor = db.cursor()
    sql = """
        INSERT INTO reports (report_type, status, created_at)
        VALUES (%s, %s, %s) RETURNING id;
    """
    params = (
        report_request.report_type,
        'Pending',
        datetime.datetime.utcnow()
    )
    cursor.execute(sql, params)
    report_id = cursor.fetchone()[0]
    db.commit()
    cursor.close()
    return get_report(db, report_id)


def get_report(db, report_id: int):
    """
    Retrieve a report by ID.

    Parameters:
    - db: Database connection.
    - report_id: ID of the report.

    Returns:
    - Report schema.
    """
    cursor = db.cursor()
    sql = """
        SELECT id, report_type, status, created_at, completed_at, file_path
        FROM reports WHERE id = %s;
    """
    cursor.execute(sql, (report_id,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return schemas.Report(
            id=row[0],
            report_type=row[1],
            status=row[2],
            created_at=row[3],
            completed_at=row[4],
            file_path=row[5]
        )
    return None


def update_report_status(db, report_id: int, status: str, file_path: str = None):
    """
    Update the status of a report.

    Parameters:
    - db: Database connection.
    - report_id: ID of the report.
    - status: New status of the report.
    - file_path: File path of the generated report, if applicable.

    Returns:
    - None
    """
    cursor = db.cursor()
    params = []
    fields = []
    if status:
        fields.append("status = %s")
        params.append(status)
    if file_path:
        fields.append("file_path = %s")
        params.append(file_path)
        fields.append("completed_at = %s")
        params.append(datetime.datetime.utcnow())
    params.append(report_id)
    sql = f"UPDATE reports SET {', '.join(fields)} WHERE id = %s;"
    cursor.execute(sql, params)
    db.commit()
    cursor.close()
