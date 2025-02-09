"""
Author: Daniel Stone

Filename: stone_requests.py

File Decription: This program fetches historical stock market data for
user-selected companies using web APIs.

Help:
    Used ChatGPT to:
                    format date properly
                    implement API headers
                    create a more specific exception

"""

from datetime import datetime
import requests


def download_data(ticker: str) -> dict:
    """
    Fetches stock market data for given ticker symbol over a five-year period

    Args:
        ticker (str): The stock's ticker symbol (e.g., 'AAPL', 'TSLA')

    Returns:
        dict: A dictionary containing stock data like min/max/avg/median price over the last year.

    """
    ticker = ticker.upper()
    today = datetime.today().date()
    start = today.replace(year=today.year - 1)  # data starts from 1 year ago

    base_url = "https://api.nasdaq.com"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit=9999"
    URL = f"{base_url}{path}"

    try:
        response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching data: {e}"}


download_data("aapl")
