"""
Utility functions for the Transaction Service.
"""

def validate_transaction_type(transaction_type: str) -> bool:
    """
    Validate the transaction type.

    Parameters:
    - transaction_type: The type of transaction ('Debit' or 'Credit').

    Returns:
    - True if valid, False otherwise.
    """
    return transaction_type in ["Debit", "Credit"]
