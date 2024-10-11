"""
Utility functions for the Inventory Service.
"""


def calculate_stock_value(quantity: int, price: float) -> float:
    """
    Calculate the total value of stock for an item.

    Parameters:
    - quantity: Quantity of the item in stock.
    - price: Price per unit of the item.

    Returns:
    - Total stock value.
    """
    return quantity * price
