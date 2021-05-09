import sys
from stock_info import StockInfo
from constants import *
from helper import get_last_n_values, get_session_data, save_session_data
import json
import time

class Trading():
    def __init__(self, ticker: str):
        self.ticker = ticker.lower()
        self.stock_info = StockInfo(self.ticker)
        self.start_time = time.time()
        self.start_session()

    def start_session(self):
        print("starting...")
        while True:
            session_data = get_session_data(self.start_time)
            signal = self.get_signal()
            print(signal)
            time.sleep(TRADE_INTERVAL)

    def get_signal(self):
        closes = self.stock_info.get_closes(PERIOD, INTERVAL)
        ema_9 = self.stock_info.get_ema(closes, 9, EMA_MULTIPLIER)
        ema_26 = self.stock_info.get_ema(closes, 26, EMA_MULTIPLIER)
        macd = self.stock_info.get_macd(ema_9, ema_26)
        signal_line = self.stock_info.get_ema(macd, SIGNAL_LINE, EMA_MULTIPLIER)

        histogram = self.stock_info.get_macd_histogram(signal_line, macd)
        if not histogram:
            return

        recent_histogram = list(get_last_n_values(histogram, 1).values())[0]
        if not recent_histogram:
            return

        if recent_histogram > 0:
            return "buy"
        else:
            return "sell"
    
    def buy_shares(self):
        pass

    def sell_shares(self):
        pass

    def end_session(self):
        pass

def __main__():
    ticker = input("Enter ticker: ")
    Trading(ticker)

if __name__ == "__main__":
    __main__()

