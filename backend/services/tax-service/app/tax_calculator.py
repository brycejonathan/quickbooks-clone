"""
Tax calculator for the Tax Service.

Contains functions for calculating taxes based on income and deductions.
"""

def calculate_income_tax(income, deductions):
    """
    Calculate income tax based on progressive tax brackets.

    Parameters:
    - income: Total income.
    - deductions: Total deductions.

    Returns:
    - Calculated tax amount.
    """
    taxable_income = max(0, income - deductions)
    tax = 0.0

    # Simplified tax brackets
    brackets = [
        (9875, 0.10),
        (40125, 0.12),
        (85525, 0.22),
        (163300, 0.24),
        (207350, 0.32),
        (518400, 0.35),
        (float('inf'), 0.37),
    ]

    previous_limit = 0
    for limit, rate in brackets:
        if taxable_income > previous_limit:
            taxable_amount = min(taxable_income, limit) - previous_limit
            tax += taxable_amount * rate
            previous_limit = limit
        else:
            break

    return tax
