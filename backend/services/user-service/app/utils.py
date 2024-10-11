"""
Utility functions for password hashing and verification.
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    """
    Hash a plaintext password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """
    Verify a plaintext password against the hashed version.
    """
    return pwd_context.verify(plain_password, hashed_password)
