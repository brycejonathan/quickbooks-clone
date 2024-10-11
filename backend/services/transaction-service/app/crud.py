"""
CRUD operations for the Transaction Service using direct AWS RDS PostgreSQL connection.
"""

from . import schemas
import datetime
import logging

logger = logging.getLogger(__name__)


def create_transaction(db, transaction: schemas.TransactionCreate):
    """
    Create a new transaction.
    """
    cursor = db.cursor()
    sql = """
        INSERT INTO transactions (description, amount, date, account_id, transaction_type)
        VALUES (%s, %s, %s, %s, %s) RETURNING id;
    """
    params = (
        transaction.description,
        transaction.amount,
        datetime.datetime.utcnow(),
        transaction.account_id,
        transaction.transaction_type
    )
    cursor.execute(sql, params)
    transaction_id = cursor.fetchone()[0]
    db.commit()
    cursor.close()
    return get_transaction(db, transaction_id)


def get_transaction(db, transaction_id: int):
    """
    Retrieve a transaction by ID.
    """
    cursor = db.cursor()
    sql = """
        SELECT id, description, amount, date, account_id, transaction_type
        FROM transactions WHERE id = %s;
    """
    cursor.execute(sql, (transaction_id,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return schemas.Transaction(
            id=row[0],
            description=row[1],
            amount=row[2],
            date=row[3],
            account_id=row[4],
            transaction_type=row[5]
        )
    return None


def update_transaction(db, transaction_id: int, transaction: schemas.TransactionUpdate):
    """
    Update an existing transaction.
    """
    cursor = db.cursor()
    fields = []
    params = []
    if transaction.description is not None:
        fields.append("description = %s")
        params.append(transaction.description)
    if transaction.amount is not None:
        fields.append("amount = %s")
        params.append(transaction.amount)
    if transaction.account_id is not None:
        fields.append("account_id = %s")
        params.append(transaction.account_id)
    if transaction.transaction_type is not None:
        fields.append("transaction_type = %s")
        params.append(transaction.transaction_type)
    params.append(transaction_id)
    sql = f"UPDATE transactions SET {', '.join(fields)} WHERE id = %s;"
    cursor.execute(sql, params)
    db.commit()
    cursor.close()
    return get_transaction(db, transaction_id)


def delete_transaction(db, transaction_id: int):
    """
    Delete a transaction.
    """
    cursor = db.cursor()
    sql = "DELETE FROM transactions WHERE id = %s;"
    cursor.execute(sql, (transaction_id,))
    db.commit()
    cursor.close()
    return cursor.rowcount > 0
