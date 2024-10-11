"""
Utility functions for the Payroll Service.
"""


def calculate_taxes(gross_pay: float) -> float:
    """
    Calculate taxes based on gross pay.

    Parameters:
    - gross_pay: Gross pay amount.

    Returns:
    - Calculated taxes.
    """
    # Simple tax calculation (e.g., 20% tax rate)
    tax_rate = 0.20
    return gross_pay * tax_rate


def calculate_deductions(gross_pay: float) -> float:
    """
    Calculate deductions based on gross pay.

    Parameters:
    - gross_pay: Gross pay amount.

    Returns:
    - Calculated deductions.
    """
    # Simple deduction calculation (e.g., 5% for benefits)
    deduction_rate = 0.05
    return gross_pay * deduction_rate
