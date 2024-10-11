"""
CRUD operations for the Banking Service using direct AWS RDS PostgreSQL connection.
"""

from . import schemas
import logging

logger = logging.getLogger(__name__)


# Bank Account CRUD Operations

def get_bank_account(db, account_id: int):
    """
    Retrieve a bank account by ID.
    """
    cursor = db.cursor()
    sql = "SELECT id, account_name, account_number, balance FROM bank_accounts WHERE id = %s;"
    cursor.execute(sql, (account_id,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return schemas.BankAccount(
            id=row[0],
            account_name=row[1],
            account_number=row[2],
            balance=float(row[3])
        )
    return None


def get_bank_account_by_number(db, account_number: str):
    """
    Retrieve a bank account by account number.
    """
    cursor = db.cursor()
    sql = "SELECT id, account_name, account_number, balance FROM bank_accounts WHERE account_number = %s;"
    cursor.execute(sql, (account_number,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return schemas.BankAccount(
            id=row[0],
            account_name=row[1],
            account_number=row[2],
            balance=float(row[3])
        )
    return None


def create_bank_account(db, bank_account: schemas.BankAccountCreate):
    """
    Create a new bank account.
    """
    cursor = db.cursor()
    sql = """
        INSERT INTO bank_accounts (account_name, account_number, balance)
        VALUES (%s, %s, %s) RETURNING id;
    """
    params = (bank_account.account_name, bank_account.account_number, bank_account.balance)
    cursor.execute(sql, params)
    account_id = cursor.fetchone()[0]
    db.commit()
    cursor.close()
    return get_bank_account(db, account_id)


# Bank Transaction CRUD Operations

def create_bank_transaction(db, transaction: schemas.BankTransactionCreate):
    """
    Create a new bank transaction.
    """
    cursor = db.cursor()
    # Insert transaction
    sql = """
        INSERT INTO bank_transactions (bank_account_id, description, amount, date, transaction_type)
        VALUES (%s, %s, %s, %s, %s) RETURNING id;
    """
    params = (
        transaction.bank_account_id,
        transaction.description,
        transaction.amount,
        datetime.datetime.utcnow(),
        transaction.transaction_type
    )
    cursor.execute(sql, params)
    transaction_id = cursor.fetchone()[0]
    # Update bank account balance
    if transaction.transaction_type == 'Credit':
        balance_update_sql = "UPDATE bank_accounts SET balance = balance + %s WHERE id = %s;"
    else:
        balance_update_sql = "UPDATE bank_accounts SET balance = balance - %s WHERE id = %s;"
    cursor.execute(balance_update_sql, (transaction.amount, transaction.bank_account_id))
    db.commit()
    cursor.close()
    return get_bank_transaction(db, transaction_id)


def get_bank_transaction(db, transaction_id: int):
    """
    Retrieve a bank transaction by ID.
    """
    cursor = db.cursor()
    sql = """
        SELECT id, bank_account_id, description, amount, date, transaction_type
        FROM bank_transactions WHERE id = %s;
    """
    cursor.execute(sql, (transaction_id,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return schemas.BankTransaction(
            id=row[0],
            bank_account_id=row[1],
            description=row[2],
            amount=float(row[3]),
            date=row[4],
            transaction_type=row[5]
        )
    return None
