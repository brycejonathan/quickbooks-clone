"""
Utility functions for the Data Quality Service.
"""

from .validators import is_positive_number, is_valid_email
from .schemas import ValidationResult, DataQualityReport, DataQualityIssue
import logging

logger = logging.getLogger(__name__)


def validate_data(data):
    """
    Validate data according to predefined rules.

    Parameters:
    - data: DataInput schema.

    Returns:
    - ValidationResult schema.
    """
    errors = []

    # Example validation rules
    if data.field_name == "email":
        if not is_valid_email(data.value):
            errors.append("Invalid email format.")
    elif data.field_name == "amount":
        if not is_positive_number(float(data.value)):
            errors.append("Amount must be a positive number.")
    else:
        errors.append(f"No validation rules defined for field '{data.field_name}'.")

    is_valid = len(errors) == 0
    return ValidationResult(is_valid=is_valid, errors=errors)


def generate_data_quality_report(db):
    """
    Generate a data quality report.

    Parameters:
    - db: Database connection.

    Returns:
    - DataQualityReport schema.
    """
    cursor = db.cursor()
    sql = "SELECT id, issue_type, description, detected_at, resolved FROM data_quality_issues;"
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()

    issues = [
        DataQualityIssue(
            id=row[0],
            issue_type=row[1],
            description=row[2],
            detected_at=row[3],
            resolved=row[4]
        )
        for row in rows
    ]

    total_issues = len(issues)
    unresolved_issues = sum(1 for issue in issues if not issue.resolved)

    report = DataQualityReport(
        total_issues=total_issues,
        unresolved_issues=unresolved_issues,
        issues=issues
    )

    return report
