import yfinance as yf
from yahoo_fin import stock_info as si
import matplotlib.pyplot as plt
import sys
from constants import *
from helper import get_last_n_values

class StockInfo:
    def __init__(self, ticker: str):
        self.ticker = ticker.lower()

    def get_prices(self, period, interval):
        return yf.download(tickers=self.ticker, period=period, interval=interval)

    def get_current_price(self):
        price = si.get_live_price(self.ticker)
        return price

    def get_closes(self, period, interval):
        closes = {}
        prices = self.get_prices(period, interval)
        for i, price in prices["Close"].items():
            closes[str(i.time())] = price
        closes = get_last_n_values(closes, MAX_VALUES)
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

    def _graph(self, chart_range, charts):
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
        plt.show(block=False)
    
    def graph_ma(self, period, interval):
        closes = self.get_closes(PERIOD, INTERVAL)
        ma_50 = self.get_ma(MA_SHORT, PERIOD, INTERVAL)
        ma_200 = self.get_ma(MA_LONG, PERIOD, INTERVAL)
        self._graph(range(0, len(closes), X_AXIS_INTERVAL), {
            "Price": {"type": "line", "data": closes}, 
            "50MA": {"type": "line", "data": ma_50},
            "200MA": {"type": "line", "data": ma_200}
        })

    def graph_ema(self, period, interval):
        closes = self.get_closes(PERIOD, INTERVAL)
        ema_9 = self.get_ema(closes, 9, EMA_MULTIPLIER)
        ema_26 = self.get_ema(closes, 26, EMA_MULTIPLIER)
        self._graph(range(0, len(closes), X_AXIS_INTERVAL), {
            "Price": {"type": "line", "data": closes}, 
            "9EMA": {"type": "line", "data": ema_9},
            "26EMA": {"type": "line", "data": ema_26},
        })

    def graph_macd(self, period, interval):
        closes = self.get_closes(PERIOD, INTERVAL)
        ema_9 = self.get_ema(closes, 9, EMA_MULTIPLIER)
        ema_26 = self.get_ema(closes, 26, EMA_MULTIPLIER)

        macd = self.get_macd(ema_9, ema_26)
        signal_line = self.get_ema(macd, SIGNAL_LINE, EMA_MULTIPLIER)
        histogram = self.get_macd_histogram(signal_line, macd)
        self._graph(range(0, len(closes), x_axis_interval), {
            "MACD": {"type": "line", "data": macd},
            "Signal Line": {"type": "line", "data": signal_line},
            "Histogram": {"type": "bar", "data": histogram}
        })

    def graph_all(self):
        closes = self.get_closes(PERIOD, INTERVAL)
        figure, axis = plt.subplots(2, 2)
       
        # MA
        
        ma_50 = self.get_ma(MA_SHORT, PERIOD, INTERVAL)
        ma_200 = self.get_ma(MA_LONG, PERIOD, INTERVAL)
        
        axis[0, 0].plot(closes.keys(), closes.values(), label="Price")
        axis[0, 0].plot(ma_50.keys(), ma_50.values(), label="50MA")
        axis[0, 0].plot(ma_200.keys(), ma_200.values(), label="200MA")
        axis[0, 0].set_title("MA")
        axis[0, 0].set_xlabel("Time")
        axis[0, 0].set_ylabel("Price")
        axis[0, 0].legend()
        axis[0, 0].set_xticks(range(0, len(closes), X_AXIS_INTERVAL))

        # EMA

        ema_9 = self.get_ema(closes, 9, EMA_MULTIPLIER)
        ema_26 = self.get_ema(closes, 26, EMA_MULTIPLIER)

        axis[0, 1].plot(closes.keys(), closes.values(), label="Price")
        axis[0, 1].plot(ema_9.keys(), ema_9.values(), label="9EMA")
        axis[0, 1].plot(ema_26.keys(), ema_26.values(), label="26EMA")
        axis[0, 1].set_title("EMA")
        axis[0, 1].set_xlabel("Time")
        axis[0, 1].set_ylabel("Price")
        axis[0, 1].legend()
        axis[0, 1].set_xticks(range(0, len(closes), X_AXIS_INTERVAL))

        # MACD

        ema_9 = self.get_ema(closes, 9, EMA_MULTIPLIER)
        ema_26 = self.get_ema(closes, 26, EMA_MULTIPLIER)

        macd = self.get_macd(ema_9, ema_26)
        signal_line = self.get_ema(macd, SIGNAL_LINE, EMA_MULTIPLIER)
        histogram = self.get_macd_histogram(signal_line, macd)

        axis[1, 0].plot(macd.keys(), macd.values(), label="MACD")
        axis[1, 0].plot(signal_line.keys(), signal_line.values(), label="Signal Line")
        bar = axis[1, 0].bar(histogram.keys(), histogram.values(), label="Histogram")

        for time, price in histogram.items():
            index = list(histogram.keys()).index(time)
            if price >= 0:
                bar[index].set_color("g")
            else:
                bar[index].set_color("r")

        axis[1, 0].set_title("MACD")
        axis[1, 0].axhline(0)
        axis[1, 0].set_xlabel("Time")
        axis[1, 0].set_ylabel("Values")
        axis[1, 0].legend()
        axis[1, 0].set_xticks(range(0, len(closes), X_AXIS_INTERVAL))

        # Other

        plt.show(block=False)

def __main__():
    while True:
        ticker = input("Enter ticker: ")
        if ticker.lower() == "exit":
            sys.exit()

        stock_info = StockInfo(ticker)
        stock_info.graph_all()

if __name__ == "__main__":
    __main__()

