"""
Author: Daniel Stone

Filename: stone_requests.py

File Decription: This program fetches historical stock market data for
user-selected companies using web APIs.

Help:
    Used ChatGPT to:
                    - format date properly
                    - implement API headers
                    - create a more specific exception
                    - learn how to calculate median
                    - raise errors in try-except statements

"""

from datetime import datetime
from statistics import median
from json import dumps  # for printing nice
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

        try:

            # Check if there is data present for given ticker
            if data['data'] is None:
                raise ValueError(f"No data available for {ticker}")

            closing_prices = []  # empty list to hold all closing prices
            for entry in data['data']['tradesTable']['rows']:
                try:
                    # convert closing price data to float, remove $ and , from data
                    closing_price = float(entry['close'].replace("$", "").replace(",", ""))
                    closing_prices.append(closing_price)  # add value to end of list
                except ValueError:
                    print(f"No value found at {entry['date']}")
                    continue  # keeps loop going

            # perform various calculations on data
            print_data = {
                "Ticker": ticker,
                "Start Date": print_date,
                "Min Price": min(closing_prices),
                "Max Price": max(closing_prices),
                "Avg Price": round((sum(closing_prices) / len(closing_prices)), 2),
                "Median Price": round(median(closing_prices), 2),
            }

            return print_data

        # handle key or value errors
        except (KeyError, ValueError) as e:
            return {"error": str(e)}

    # handle issues related to opening data
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching data: {e}"}


print(dumps(download_data("aapl"), indent=2))
