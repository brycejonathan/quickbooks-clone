"""
Utility functions for the Tax Service.
"""

from .tax_calculator import calculate_income_tax
from .schemas import TaxCalculationResult, TaxFilingResult
import datetime
import logging

logger = logging.getLogger(__name__)


def calculate_tax(tax_request):
    """
    Calculate tax based on income and deductions.

    Parameters:
    - tax_request: TaxCalculationRequest schema.

    Returns:
    - TaxCalculationResult schema.
    """
    taxable_income = max(0, tax_request.income - tax_request.deductions)
    tax_due = calculate_income_tax(tax_request.income, tax_request.deductions)
    return TaxCalculationResult(
        taxable_income=taxable_income,
        tax_due=tax_due
    )


def file_tax_return(tax_filing):
    """
    File a tax return.

    Parameters:
    - tax_filing: TaxFiling schema.

    Returns:
    - TaxFilingResult schema.
    """
    # Placeholder for actual filing logic
    filing_id = 12345  # Simulated filing ID
    status = "Filed"
    filed_at = datetime.datetime.utcnow().isoformat()

    # Log the filing
    logger.info(f"Tax return filed for user {tax_filing.user_id} for year {tax_filing.filing_year}")

    return TaxFilingResult(
        filing_id=filing_id,
        status=status,
        filed_at=filed_at
    )
