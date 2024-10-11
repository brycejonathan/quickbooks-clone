"""
CRUD operations for the User Service using direct AWS RDS PostgreSQL connection.
"""

from . import schemas, utils
import logging

logger = logging.getLogger(__name__)


def get_user_by_email(db, email: str):
    """
    Retrieve a user by email.
    """
    cursor = db.cursor()
    sql = "SELECT id, email, full_name, hashed_password, is_active, is_superuser FROM users WHERE email = %s;"
    cursor.execute(sql, (email,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return schemas.User(
            id=row[0],
            email=row[1],
            full_name=row[2],
            is_active=row[4],
            is_superuser=row[5]
        ), row[3]  # Return user schema and hashed password
    return None, None


def create_user(db, user: schemas.UserCreate):
    """
    Create a new user.
    """
    cursor = db.cursor()
    sql = """
        INSERT INTO users (email, full_name, hashed_password, is_active, is_superuser)
        VALUES (%s, %s, %s, %s, %s) RETURNING id;
    """
    params = (
        user.email,
        user.full_name,
        user.password,
        True,
        False
    )
    cursor.execute(sql, params)
    user_id = cursor.fetchone()[0]
    db.commit()
    cursor.close()
    return get_user(db, user_id)


def get_user(db, user_id: int):
    """
    Retrieve a user by ID.
    """
    cursor = db.cursor()
    sql = "SELECT id, email, full_name, is_active, is_superuser FROM users WHERE id = %s;"
    cursor.execute(sql, (user_id,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return schemas.User(
            id=row[0],
            email=row[1],
            full_name=row[2],
            is_active=row[3],
            is_superuser=row[4]
        )
    return None


def authenticate_user(db, email: str, password: str):
    """
    Authenticate a user by email and password.
    """
    user_schema, hashed_password = get_user_by_email(db, email)
    if not user_schema:
        return None
    if not utils.verify_password(password, hashed_password):
        return None
    return user_schema
