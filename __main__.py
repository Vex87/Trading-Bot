import yfinance as yf
import matplotlib.pyplot as plt
from constants import *
import json

def get_last_n_values(dic, n: int):
    new_dic = {}
    for i in list(dic)[len(dic) - n:]:
        new_dic[i] = dic.get(i)
    return new_dic

class Stock:
    def __init__(self, ticker: str):
        self.ticker = ticker.lower()

    def get_prices(self, period, interval):
        return yf.download(tickers=self.ticker, period=period, interval=interval)

    def get_closes(self, period, interval):
        closes = {}
        prices = self.get_prices(period, interval)
        for i, price in prices["Close"].items():
            closes[str(i.time())] = price
        return closes

    def get_ma(self, ma_amount, period, interval):
        ma_prices = {}
        ma_avgs = {}
        prices = self.get_closes(period, interval)
        
        for time, price in prices.items():
            ma_prices[time] = price
            if len(ma_prices) < ma_amount:
                continue
            else:
                ma_avgs[time] = sum(get_last_n_values(ma_prices, ma_amount).values()) / ma_amount
        
        return ma_avgs

    def graph(self, chart_range, charts):
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.title(self.ticker.upper())
    
        for name, chart in charts.items():
            plt.plot(chart.keys(), chart.values(), label=name)
       
        plt.xticks(chart_range)
        plt.legend()
        plt.show()

    def graph_ma(self, period, interval):
        closes = self.get_closes(PERIOD, INTERVAL)
        ma_50 = self.get_ma(MA_SHORT, PERIOD, INTERVAL)
        ma_200 = self.get_ma(MA_LONG, PERIOD, INTERVAL)
        self.graph(range(0, len(closes), X_AXIS_INTERVAL), {
            "Price": closes, 
            "50MA": ma_50,
            "200MA": ma_200
        })

def __main__():
    ticker = input("Enter ticker: ")
    stock_info = Stock(ticker)
    stock_info.graph_ma(PERIOD, INTERVAL)

if __name__ == "__main__":
    __main__()

