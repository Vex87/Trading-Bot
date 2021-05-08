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

    def get_ema(self, prices, ema_amount: int, multiplier: int):
        ema_prices = {}
        ema_avgs = {}
        multiplier = 2 / (ema_amount + 1)

        for time, price in prices.items():
            ema_prices[time] = price
            if len(ema_prices) < ema_amount:
                continue
            elif len(ema_prices) == ema_amount:
                ema_avgs[time] = sum(get_last_n_values(ema_prices, ema_amount).values()) / ema_amount
            else:
                ema_avgs[time] = price * multiplier + sum(get_last_n_values(ema_avgs, 1).values()) * (1 - multiplier)

        return ema_avgs
   
    def get_macd(self, ema_26, ema_9):
        macd = {}
        for time, ema_9_price in ema_9.items():
            ema_26_price = ema_26.get(time)
            if ema_26_price:
                macd[time] = ema_26_price - ema_9_price
        return macd

    def get_macd_histogram(self, macd, signal_line):
        histogram = {}
        for time, macd_value in macd.items():
            signal_line_value = signal_line.get(time)
            if signal_line_value:
                histogram[time] = signal_line_value - macd_value
        return histogram

    def graph(self, chart_range, charts):
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.title(self.ticker.upper())
    
        for name, info in charts.items():
            info_type = info.get("type")
            info_data = info.get("data")
            if not info_type or not info_data:
                continue

            if info_type == "line":
                plt.plot(info_data.keys(), info_data.values(), label=name)
            elif info_type == "bar":
                bar = plt.bar(info_data.keys(), info_data.values(), label=name)
                for time, price in info_data.items():
                    index = list(info_data.keys()).index(time)
                    if price >= 0:
                        bar[index].set_color("g")
                    else:
                        bar[index].set_color("r")

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

    def graph_ema(self, period, interval):
        closes = self.get_closes(PERIOD, INTERVAL)
        ema_9 = self.get_ema(closes, 9, EMA_MULTIPLIER)
        ema_26 = self.get_ema(closes, 26, EMA_MULTIPLIER)
        self.graph(range(0, len(closes), X_AXIS_INTERVAL), {
            "Price": closes, 
            "9EMA": ema_9,
            "26EMA": ema_26,
        })

    def graph_macd(self, period, interval):
        closes = self.get_closes(PERIOD, INTERVAL)
        ema_9 = self.get_ema(closes, 9, EMA_MULTIPLIER)
        ema_26 = self.get_ema(closes, 26, EMA_MULTIPLIER)

        macd = self.get_macd(ema_9, ema_26)
        signal_line = self.get_ema(macd, SIGNAL_LINE, EMA_MULTIPLIER)
        histogram = self.get_macd_histogram(signal_line, macd)
        self.graph(range(0, len(closes), X_AXIS_INTERVAL), {
            "MACD": {"type": "line", "data": macd},
            "Signal Line": {"type": "line", "data": signal_line},
            "Histogram": {"type": "bar", "data": histogram}
        })

def __main__():
    ticker = input("Enter ticker: ")
    stock_info = Stock(ticker)
    stock_info.graph_macd(PERIOD, INTERVAL)

if __name__ == "__main__":
    __main__()

