"""
Utility functions for the Ledger Service.
"""

def calculate_balance(debits: float, credits: float) -> float:
    """
    Calculate the balance given debits and credits.

    Parameters:
    - debits: Total debit amount.
    - credits: Total credit amount.

    Returns:
    - Calculated balance.
    """
    return debits - credits
