"""
Validators for the Data Quality Service.

Contains functions for validating data according to predefined rules.
"""


def is_positive_number(value):
    """
    Check if the value is a positive number.

    Parameters:
    - value: The value to check.

    Returns:
    - True if positive number, False otherwise.
    """
    return isinstance(value, (int, float)) and value > 0


def is_valid_email(email):
    """
    Validate email format.

    Parameters:
    - email: The email address to validate.

    Returns:
    - True if valid email, False otherwise.
    """
    import re
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.match(pattern, email) is not None
