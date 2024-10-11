"""
Pydantic schemas for data validation and serialization.
"""

from pydantic import BaseModel, EmailStr
import datetime


# Employee Schemas

class EmployeeBase(BaseModel):
    """
    Base schema for Employee containing common fields.
    """
    full_name: str
    email: EmailStr
    position: str
    salary: float


class EmployeeCreate(EmployeeBase):
    """
    Schema for creating a new employee.
    """
    date_hired: datetime.date


class Employee(EmployeeBase):
    """
    Schema representing an employee.
    """
    id: int
    date_hired: datetime.date

    class Config:
        orm_mode = True


# Payroll Schemas

class PayrollBase(BaseModel):
    """
    Base schema for Payroll containing common fields.
    """
    employee_id: int
    pay_date: datetime.date


class PayrollCreate(PayrollBase):
    """
    Schema for creating a new payroll record.
    """
    pass


class PayrollRecord(PayrollBase):
    """
    Schema representing a payroll record.
    """
    id: int
    gross_pay: float
    net_pay: float
    deductions: float
    taxes: float

    class Config:
        orm_mode = True
