"""
Utility functions for the Accounting Service.
"""


def calculate_net_income(revenues: float, expenses: float) -> float:
    """
    Calculate net income.

    Parameters:
    - revenues: Total revenues.
    - expenses: Total expenses.

    Returns:
    - Net income.
    """
    return revenues - expenses
