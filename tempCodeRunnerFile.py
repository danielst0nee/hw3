"""
Author: Daniel Stone

Filename: stone_requests.py

File Decription: This program fetches historical stock market data for
user-selected companies using web APIs.

Help:
"""

import requests
from datetime import datetime


def download_data(ticker: str) -> dict:
    """
    Fetches stock market data for given ticker symbol over a five-year period

    Args:
        ticker (str): The stock's ticker symbol (e.g., 'AAPL', 'TSLA')

    Returns:
        dict: A dictionary containing stock data like min/max/avg/median price over the last five years.

    """
    ticker = ticker.upper()
    today = datetime.today()
    start = str(today.replace(year=today.year - 1))
    base_url = "https://api.nasdaq.com"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit=9999"
    URL = f"{base_url}/{path}"

    try:
        response = requests.get(URL)
        print(response.json())
    except Exception as e:
        print(e)


download_data('aapl')
