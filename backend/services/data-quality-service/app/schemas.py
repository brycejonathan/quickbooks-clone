"""
Pydantic schemas for data validation and serialization.
"""

from pydantic import BaseModel
from typing import List


class DataInput(BaseModel):
    """
    Schema representing input data to be validated.
    """
    field_name: str
    value: str


class ValidationResult(BaseModel):
    """
    Schema representing the result of data validation.
    """
    is_valid: bool
    errors: List[str] = []


class DataQualityIssue(BaseModel):
    """
    Schema representing a data quality issue.
    """
    id: int
    issue_type: str
    description: str
    detected_at: str
    resolved: bool


class DataQualityReport(BaseModel):
    """
    Schema representing a data quality report.
    """
    total_issues: int
    unresolved_issues: int
    issues: List[DataQualityIssue]
