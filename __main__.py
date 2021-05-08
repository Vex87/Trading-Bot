import yfinance as yf
import matplotlib.pyplot as plt
from constants import *

def get_prices(ticker: str):
    ticker = ticker.lower()
    data = yf.download(tickers = ticker, period = TICKER_PERIOD, interval = TICKER_INTERVAL)
    return data

def get_closes(data):
    closes = []
    for price in data["Close"]:
        closes.append(price)
    return closes

def graph_closes(closes):
    times = [time for time in range(len(closes))]
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.title("Stock Prices")
    plt.xlim(0, len(closes))
    plt.plot(times, closes)
    plt.show()

def __main__():
    ticker = input("Enter ticker: ")
    data = get_prices(ticker)
    closes = get_closes(data)
    graph_closes(closes)

if __name__ == "__main__":
    __main__()

