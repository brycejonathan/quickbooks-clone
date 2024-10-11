"""
Utility functions for the Audit Service.
"""


def format_audit_details(details: dict) -> str:
    """
    Format audit details from a dictionary to a JSON string.

    Parameters:
    - details: Dictionary containing audit details.

    Returns:
    - JSON-formatted string.
    """
    import json
    return json.dumps(details, indent=2)
