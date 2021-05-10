import sys
import time
from helper import get_session_data

def __main__():
    while True:
        input_text = input("> ")
        if input_text == "exit":
            sys.exit()
        elif input_text:
            session_data = get_session_data(int(input_text))
            if not session_data:
                print(f"Could not find session {input_text}")

            start_time = time.ctime(session_data["start_time"])
            starting_balance = session_data["starting_balance"]
            balance = round(session_data["balance"], 2)
            profit = round(balance - starting_balance, 2)
            shares = session_data["shares"]
            
            print(f"Start Time: {start_time}")
            print(f"Starting Balance: ${starting_balance}")
            print(f"Balance: ${balance}")
            print(f"Profit: ${profit}")
            print(f"Shares: {shares}")

            trades_count = len(session_data["trades"])
            if trades_count < 2:
                print("Not enough trades to show more data")
                continue

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
                    except:
                        pass

            win_rate = round(win_trades / (win_trades + loss_trades), 4) * 100
            price_change = session_data["trades"][-1]["price"] - session_data["trades"][0]["price"]

            print(f"Trades: {trades_count}")
            print(f"Win Trades: {win_trades}")
            print(f"Loss Trades: {loss_trades}")
            print(f"Win Rate: {win_rate}%")
            print(f"Price Change: ${price_change}")

if __name__ == "__main__":
    __main__()