"""
Report export module for the Reporting Service.

Contains functions for exporting reports in various formats.
"""

import csv
import json
import io


def export_report_csv(report_data):
    """
    Export report data to CSV format.

    Parameters:
    - report_data: List of dictionaries representing report data.

    Returns:
    - CSV formatted string.
    """
    if not report_data:
        return ""

    output = io.StringIO()
    fieldnames = report_data[0].keys()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(report_data)
    return output.getvalue()


def export_report_json(report_data):
    """
    Export report data to JSON format.

    Parameters:
    - report_data: List of dictionaries representing report data.

    Returns:
    - JSON formatted string.
    """
    return json.dumps(report_data, indent=2)
