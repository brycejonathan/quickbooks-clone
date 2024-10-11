"""
Utility functions for the Banking Service.
"""

from .crud import get_bank_account, get_bank_transaction
import logging

logger = logging.getLogger(__name__)


def reconcile_bank_account(db, account_id: int) -> bool:
    """
    Reconcile a bank account by verifying transactions.

    Parameters:
    - account_id: ID of the bank account to reconcile.

    Returns:
    - True if reconciliation is successful, False otherwise.
    """
    bank_account = get_bank_account(db, account_id)
    if not bank_account:
        return False
    cursor = db.cursor()
    sql = """
        SELECT amount, transaction_type FROM bank_transactions
        WHERE bank_account_id = %s;
    """
    cursor.execute(sql, (account_id,))
    transactions = cursor.fetchall()
    cursor.close()
    calculated_balance = 0.0
    for amount, transaction_type in transactions:
        if transaction_type == 'Credit':
            calculated_balance += float(amount)
        else:
            calculated_balance -= float(amount)
    # Update the bank account balance
    cursor = db.cursor()
    update_sql = "UPDATE bank_accounts SET balance = %s WHERE id = %s;"
    cursor.execute(update_sql, (calculated_balance, account_id))
    db.commit()
    cursor.close()
    return True
