import sys
from stock_info import StockInfo
from constants import *
from helper import get_last_n_values, get_session_data, save_session_data
import json
import time

class Trading():
    def __init__(self, ticker: str, starting_balance: int):
        self.ticker = ticker.lower()
        self.stock_info = StockInfo(self.ticker)
        self.start_time = round(time.time())
        self.starting_balance = starting_balance
        self.start_session()

    def start_session(self):
        print("starting...")

        self.session_data = get_session_data(self.start_time)
        self.session_data["start_time"] = self.start_time
        self.session_data["ticker"] = self.ticker
        self.session_data["starting_balance"] = self.starting_balance
        self.session_data["balance"] = self.starting_balance
        save_session_data(self.session_data)

        while True:
            self.session_data = get_session_data(self.start_time)
            signal = self.get_signal()
            if signal == "buy" and self.session_data["shares"] == 0:
                self.buy_shares()
            elif signal == "sell" and self.session_data["shares"] > 0:
                self.sell_shares()

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
        price = self.stock_info.get_current_price()
        shares_to_buy = self.session_data["balance"] / price
        money_to_spend = int(self.session_data["balance"])
        self.session_data["shares"] = shares_to_buy
        self.session_data["balance"] = 0
        save_session_data(self.session_data)
        print(f"Bought {shares_to_buy} shares of {self.ticker} at ${price} (-${money_to_spend})")

    def sell_shares(self):
        price = self.stock_info.get_current_price()
        shares_to_sell = str(self.session_data["shares"])
        money_to_earn = price * self.session_data["shares"]
        self.session_data["shares"] = 0
        self.session_data["balance"] = money_to_earn
        save_session_data(self.session_data)
        print(f"Sold {shares_to_sell} shares of {self.ticker} at ${price} (+${money_to_earn})")

    def end_session(self):
        pass

def __main__():
    ticker = input("Enter ticker: ")
    starting_balance = int(input("Enter starting balance: "))
    Trading(ticker, starting_balance)

if __name__ == "__main__":
    __main__()

