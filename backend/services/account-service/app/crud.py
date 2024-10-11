"""
CRUD operations and data aggregation for the Accounting Service using direct AWS RDS PostgreSQL connection.
"""

from . import schemas
import logging

logger = logging.getLogger(__name__)


def generate_balance_sheet(db):
    """
    Generate the balance sheet by calculating total assets, liabilities, and equity.

    Returns:
    - BalanceSheet schema.
    """
    cursor = db.cursor()
    try:
        # Calculate assets
        cursor.execute("SELECT SUM(balance) FROM accounts WHERE type = 'Asset';")
        assets = cursor.fetchone()[0] or 0.0

        # Calculate liabilities
        cursor.execute("SELECT SUM(balance) FROM accounts WHERE type = 'Liability';")
        liabilities = cursor.fetchone()[0] or 0.0

        # Calculate equity
        cursor.execute("SELECT SUM(balance) FROM accounts WHERE type = 'Equity';")
        equity = cursor.fetchone()[0] or 0.0

        balance_sheet = schemas.BalanceSheet(
            assets=assets,
            liabilities=liabilities,
            equity=equity
        )
        return balance_sheet
    finally:
        cursor.close()


def generate_income_statement(db):
    """
    Generate the income statement by calculating total revenues and expenses.

    Returns:
    - IncomeStatement schema.
    """
    cursor = db.cursor()
    try:
        # Calculate revenues
        cursor.execute("""
            SELECT SUM(amount) FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            WHERE a.type = 'Revenue' AND t.transaction_type = 'Credit';
        """)
        revenues = cursor.fetchone()[0] or 0.0

        # Calculate expenses
        cursor.execute("""
            SELECT SUM(amount) FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            WHERE a.type = 'Expense' AND t.transaction_type = 'Debit';
        """)
        expenses = cursor.fetchone()[0] or 0.0

        net_income = revenues - expenses

        income_statement = schemas.IncomeStatement(
            revenues=revenues,
            expenses=expenses,
            net_income=net_income
        )
        return income_statement
    finally:
        cursor.close()
