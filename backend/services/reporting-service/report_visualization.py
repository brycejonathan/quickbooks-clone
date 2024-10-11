"""
Report visualization module for the Reporting Service.

Contains functions for generating visual representations of reports.
"""

import matplotlib.pyplot as plt
import io
import base64


def generate_bar_chart(data, title):
    """
    Generate a bar chart from the provided data.

    Parameters:
    - data: Dictionary with keys as labels and values as amounts.
    - title: Title of the chart.

    Returns:
    - Base64 encoded image of the bar chart.
    """
    labels = list(data.keys())
    amounts = list(data.values())

    plt.figure(figsize=(10, 6))
    plt.bar(labels, amounts, color='blue')
    plt.title(title)
    plt.xlabel('Categories')
    plt.ylabel('Amount')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return image_base64
