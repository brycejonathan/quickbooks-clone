"""
CRUD operations for the Ledger Service using direct AWS RDS PostgreSQL connection.
"""

from . import schemas
import logging

logger = logging.getLogger(__name__)


def get_account(db, account_id: int):
    """
    Retrieve an account by ID.
    """
    cursor = db.cursor()
    sql = "SELECT id, name, type, balance FROM accounts WHERE id = %s;"
    cursor.execute(sql, (account_id,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return schemas.Account(
            id=row[0],
            name=row[1],
            type=row[2],
            balance=float(row[3])
        )
    return None


def get_account_by_name(db, name: str):
    """
    Retrieve an account by name.
    """
    cursor = db.cursor()
    sql = "SELECT id, name, type, balance FROM accounts WHERE name = %s;"
    cursor.execute(sql, (name,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return schemas.Account(
            id=row[0],
            name=row[1],
            type=row[2],
            balance=float(row[3])
        )
    return None


def create_account(db, account: schemas.AccountCreate):
    """
    Create a new account.
    """
    cursor = db.cursor()
    sql = """
        INSERT INTO accounts (name, type, balance)
        VALUES (%s, %s, %s) RETURNING id;
    """
    params = (account.name, account.type, account.balance)
    cursor.execute(sql, params)
    account_id = cursor.fetchone()[0]
    db.commit()
    cursor.close()
    return get_account(db, account_id)


def update_account(db, account_id: int, account: schemas.AccountUpdate):
    """
    Update an existing account.
    """
    cursor = db.cursor()
    fields = []
    params = []
    if account.name is not None:
        fields.append("name = %s")
        params.append(account.name)
    if account.type is not None:
        fields.append("type = %s")
        params.append(account.type)
    if account.balance is not None:
        fields.append("balance = %s")
        params.append(account.balance)
    params.append(account_id)
    sql = f"UPDATE accounts SET {', '.join(fields)} WHERE id = %s;"
    cursor.execute(sql, params)
    db.commit()
    cursor.close()
    return get_account(db, account_id)


def delete_account(db, account_id: int):
    """
    Delete an account.
    """
    cursor = db.cursor()
    sql = "DELETE FROM accounts WHERE id = %s;"
    cursor.execute(sql, (account_id,))
    db.commit()
    cursor.close()
    return cursor.rowcount > 0
