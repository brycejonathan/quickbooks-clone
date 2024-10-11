"""
Pydantic schemas for data validation and serialization.
"""

from pydantic import BaseModel
from typing import List


class AuditLogBase(BaseModel):
    """
    Base schema for AuditLog containing common fields.
    """
    user_id: int = None
    action: str
    details: str = None


class AuditLogCreate(AuditLogBase):
    """
    Schema for creating a new audit log entry.
    """
    pass


class AuditLog(AuditLogBase):
    """
    Schema representing an audit log entry.
    """
    id: int
    timestamp: str

    class Config:
        orm_mode = True


class AuditLogList(BaseModel):
    """
    Schema representing a list of audit logs.
    """
    audit_logs: List[AuditLog]
