"""
Pydantic schemas for data validation and serialization.
"""

from pydantic import BaseModel
import datetime

class ReportBase(BaseModel):
    """
    Base schema for Report containing common fields.
    """
    report_type: str  # e.g., 'balance_sheet', 'income_statement'

class ReportCreate(ReportBase):
    """
    Schema for creating a new report request.
    """
    pass

class Report(ReportBase):
    """
    Schema representing a report.
    """
    id: int
    status: str
    created_at: datetime.datetime
    completed_at: datetime.datetime = None
    file_path: str = None

    class Config:
        orm_mode = True
