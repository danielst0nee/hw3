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
                    learn how to calculate median

"""

from datetime import datetime
from statistics import median
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
    print_date = start.strftime("%m-%d-%Y")

    base_url = "https://api.nasdaq.com"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit=9999"
    URL = f"{base_url}{path}"

    try:
        response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})  # added API headers
        data = response.json()

        if data['data'] is None:
            return {"error": f"No data available for {ticker}"}

        # accesses first entry
        # print(data['data']['tradesTable']['rows'][0])

        closing_prices = []  # empty list to hold all closing prices
        for entry in data['data']['tradesTable']['rows']:
            closing_price = float(entry['close'].replace("$", "").replace(",", ""))
            closing_prices.append(closing_price)

        print_data = {
            "Ticker": ticker,
            "Start Date": print_date,
            "Min Price": min(closing_prices),
            "Max Price": max(closing_prices),
            "Avg Price": round((sum(closing_prices) / len(closing_prices)), 2),
            "Median Price": round(median(closing_prices), 2),
        }

        return print_data
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching data: {e}"}


print(download_data("aapl"))
