"""
Utility functions for the Integration Service.
"""

import requests
import logging

logger = logging.getLogger(__name__)


def sync_integration_data(integration):
    """
    Synchronize data with the external service.

    Parameters:
    - integration: Integration schema.

    Returns:
    - None
    """
    # Placeholder for actual synchronization logic
    logger.info(f"Synchronizing data for integration '{integration.name}'")
    # Example: Send a GET request to the endpoint URL
    response = requests.get(integration.endpoint_url)
    if response.status_code == 200:
        logger.info(f"Data synchronized successfully for integration '{integration.name}'")
        # Update last_synced timestamp in the database if needed
    else:
        logger.error(f"Failed to synchronize data for integration '{integration.name}'")
        raise Exception("Synchronization failed")
