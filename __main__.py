import yfinance as yf
from constants import *

def get_prices(ticker: str):
    ticker = ticker.lower()
    data = yf.download(tickers = ticker, period = TICKER_PERIOD, interval = TICKER_INTERVAL)
    return data

def get_closes(data):
    closes = []
    for price in data["Close"].items():
        closes.append(price[1])
    return closes

def __main__():
    ticker = input("Enter ticker: ")
    data = get_prices(ticker)
    closes = get_closes(data)
    print(closes)

if __name__ == "__main__":
    __main__()

