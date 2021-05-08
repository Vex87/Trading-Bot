import yfinance as yf
import matplotlib.pyplot as plt
from constants import *

def get_prices(ticker: str):
    ticker = ticker.lower()
    data = yf.download(tickers = ticker, period = TICKER_PERIOD, interval = TICKER_INTERVAL)
    return data

def get_closes(data):
    closes = {}
    for i, price in data["Close"].items():
        closes[str(i.time())] = price
    return closes

def get_last_n_values(dic, n: int):
    new_dic = {}
    for i in list(dic)[len(dic) - n:]:
        new_dic[i] = dic.get(i)
    return new_dic

def graph_closes(closes):
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.title("Stock Prices")
    plt.xlim(0, len(closes))
    plt.plot(closes.keys(), closes.values())
    plt.show()

def __main__():
    ticker = input("Enter ticker: ")
    data = get_prices(ticker)
    closes = get_closes(data)
    closes = get_last_n_values(closes, 20)
    graph_closes(closes)

if __name__ == "__main__":
    __main__()

