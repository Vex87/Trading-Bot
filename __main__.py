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

def graph_charts(*charts):
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.title("Stock Prices")
    
    for chart in charts:
        plt.plot(chart.keys(), chart.values())
    
    plt.show()

def get_ma(prices, ma_amount: int):
    ma_prices = {}
    ma_avgs = {}
    for time, price in prices.items():
        ma_prices[time] = price
        if len(ma_prices) < ma_amount:
            continue
        else:
            ma_avgs[time] = sum(get_last_n_values(ma_prices, ma_amount).values()) / ma_amount
    return ma_avgs

def __main__():
    ticker = input("Enter ticker: ")
    data = get_prices(ticker)
    closes = get_closes(data)
    closes = get_last_n_values(closes, 50)
    ma_12 = get_ma(closes, 12)
    ma_26 = get_ma(closes, 26)
    graph_charts(closes, ma_12, ma_26)

if __name__ == "__main__":
    __main__()

