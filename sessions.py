import sys
import time
import math
import matplotlib.pyplot as plt
from helper import get_session_data, get_all_sessions, attach_prefix_to_number, attach_suffix_to_number
from stock_info import StockInfo

def get_session_info(start_time: int):
    session_data = get_session_data(int(start_time))
    if not session_data:
        print(f"Could not find session {start_time}")
        return

    stock_info = StockInfo(session_data["ticker"])
    stock_price = round(stock_info.get_current_price(), 2)

    start_time = time.ctime(session_data["start_time"])
    starting_balance = session_data["starting_balance"]
    balance = round(session_data["balance"], 2)
    shares = session_data["shares"]
    wealth = (shares * stock_price) + balance
    profit = round(wealth - starting_balance, 2)
    profit_percent = round((wealth - starting_balance) / starting_balance * 100)

    starting_balance = attach_prefix_to_number(starting_balance, "$")
    balance = attach_prefix_to_number(balance, "$")
    wealth = attach_prefix_to_number(wealth, "$")
    profit = attach_prefix_to_number(profit, "$")
    profit_percent = attach_suffix_to_number(profit_percent, "%")

    print(f"Start Time: {start_time}")
    print(f"Wealth: {wealth}")
    print(f"Starting Balance: {starting_balance}")
    print(f"Balance: {balance}")
    print(f"Profit: {profit}")
    print(f"Shares: {shares}")

    trades_count = math.floor(len(session_data["trades"]) / 2)
    if trades_count < 1:
        return

    trades = []
    win_trades = 0
    loss_trades = 0
    for i, buy_trade in enumerate(session_data["trades"]):
        if buy_trade["type"] == "buy":
            try:    
                sell_trade = session_data["trades"][i + 1]
                if sell_trade["price"] >= buy_trade["price"]:
                    win_trades += 1
                else:
                    loss_trades += 1
            except IndexError:
                pass

    win_rate = round(win_trades / (win_trades + loss_trades) * 100, 2)
    price_change = round((session_data["trades"][-1]["price"] - session_data["trades"][0]["price"]), 2)
    
    win_rate = attach_suffix_to_number(win_rate, "%")
    price_change = attach_prefix_to_number(price_change, "$")

    print(f"Trades: {trades_count}")
    print(f"Win Trades: {win_trades}")
    print(f"Loss Trades: {loss_trades}")
    print(f"Win Rate: {win_rate}")
    print(f"Price Change: {price_change}")

def get_session_trades(start_time: int):
    session_data = get_session_data(int(start_time))
    if not session_data:
        print(f"Could not find session {start_time}")
        return

    for i, buy_trade in enumerate(session_data["trades"]):
        if buy_trade["type"] == "buy":
            try:
                sell_trade = session_data["trades"][i + 1]
                
                buy_price = buy_trade["price"]
                sell_price = sell_trade["price"]
                profit = round(sell_price - buy_price, 2)
                profit_percent = round(profit / buy_price * 100, 2)

                buy_price = attach_prefix_to_number(buy_price, "$")
                sell_price = attach_prefix_to_number(sell_price, "$")
                profit = attach_prefix_to_number(profit, "$")
                profit_percent = attach_suffix_to_number(profit_percent, "%")

                print(f"{buy_price} -> {sell_price} | {profit} ({profit_percent})")            
            except IndexError:
                pass

def get_session_charts(start_time: int):
    session_data = get_session_data(int(start_time))
    if not session_data:
        print(f"Could not find session {start_time}")
        return

    balance_history = {}
    for sell_trade in session_data["trades"]:
        if sell_trade["type"] == "sell":
            balance_history[sell_trade["time"]] = float(sell_trade["shares"]) * float(sell_trade["price"])

    figure, axis = plt.subplots(2, 2)
    axis[0, 0].plot(balance_history.keys(), balance_history.values(), label="Balance")
    axis[0, 0].set_title("Balance")
    axis[0, 0].set_xlabel("Time")
    axis[0, 0].set_ylabel("Balance")
    axis[0, 0].legend()
    plt.show(block=False)

def getallsessions():
    for session_data in get_all_sessions():
        stock_info = StockInfo(session_data["ticker"])
        stock_price = round(stock_info.get_current_price(), 2)

        start_time_raw = session_data["start_time"]
        start_time = time.ctime(start_time_raw)
        starting_balance = session_data["starting_balance"]
        balance = round(session_data["balance"], 2)
        shares = session_data["shares"]
        wealth = round((shares * stock_price) + balance, 2)
        profit = round(wealth - starting_balance, 2)
        profit_percent = round((wealth - starting_balance) / starting_balance * 100)

        wealth = attach_prefix_to_number(wealth, "$")
        profit = attach_prefix_to_number(profit, "$")
        profit_percent = attach_suffix_to_number(profit_percent, "%")
    
        print(f"{start_time_raw} ({start_time}) | {wealth} | {profit} ({profit_percent})")

def __main__():
    while True:
        input_text = input("$ ")
        arguments = input_text.split(" ")
        command = arguments[0]
        
        if command == "help":
            print("getallsessions                   Gets start times for all stored sessions.")
            print("getsessioninfo <start_time>      Gets info for a session.")
            print("getsessiontrades <start_time>    Gets all trades for a session.")
            print("getsessioncharts <start_time>    Gets a chart for all trades of a session.")
            print("help                             Shows this menu.")
            print("exit                             Stops the script.")
        elif command == "getallsessions":
            getallsessions()
        elif command == "getsessioninfo":
            if len(arguments) < 2:
                print("Missing argument: session start_time")
                continue
            get_session_info(arguments[1])
        elif command == "getsessiontrades":
            if len(arguments) < 2:
                print("Missing argument: session start_time")
                continue
            get_session_trades(arguments[1])
        elif command == "getsessioncharts":
            if len(arguments) < 2:
                print("Missing argument: session start_time")
                continue
            get_session_charts(arguments[1])
        elif command == "exit":
            sys.exit()
        else:
            print("Invalid command")

if __name__ == "__main__":
    __main__()
