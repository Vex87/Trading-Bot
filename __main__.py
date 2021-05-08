import yfinance as yf
from constants import *

def get_prices(ticker: str):
    ticker = ticker.lower()
    data = yf.download(tickers = ticker, period = TICKER_PERIOD, interval = TICKER_INTERVAL)
    return data

def __main__():
    ticker = input("Enter ticker: ")
    data = get_prices(ticker)
    print(data)

if __name__ == "__main__":
    __main__()

