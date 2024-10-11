"""
Pydantic schemas for data validation and serialization.
"""

from pydantic import BaseModel


class TaxCalculationRequest(BaseModel):
    """
    Schema representing a tax calculation request.
    """
    income: float
    deductions: float


class TaxCalculationResult(BaseModel):
    """
    Schema representing the result of a tax calculation.
    """
    taxable_income: float
    tax_due: float


class TaxFiling(BaseModel):
    """
    Schema representing a tax filing request.
    """
    user_id: int
    filing_year: int
    income: float
    deductions: float


class TaxFilingResult(BaseModel):
    """
    Schema representing the result of a tax filing.
    """
    filing_id: int
    status: str
    filed_at: str
