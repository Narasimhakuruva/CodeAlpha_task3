import requests
from prettytable import PrettyTable

# API Key and base url for Alpha Vantage
API_KEY = "0MTBKMURFLQMLMAQ"
BASE_URL = "https://www.alphavantage.co/query"

# Portfolio dictionary to store stock data
portfolio_dict = {}

# Fetching/getting stock price from API

def fetch_stock_price(symbol):
    parameters = { # parameters for API request
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": API_KEY
    }
    try: # try-except block to handle exceptions/errors
        response_res = requests.get(BASE_URL, params=parameters) #requesting API
        data = response_res.json() #converting response to json formet
        if "Global Quote" in data and "05. price" in data["Global Quote"]:
            return float(data["Global Quote"]["05. price"])
        else:
            print(f"Unable to fetch data for {symbol}. Check the symbol or API limits.")
            return None
    except requests.exceptions.RequestException as e: 
        print(f"Error fetching stock data: {e}")
        return None

# Adding  stocks to the portfolio

def add_stock_to_portfolio(symbol, quantity, purchase_price):
    symbol = symbol.upper()
    if symbol in portfolio_dict:
        total_quantity = portfolio_dict[symbol]["quantity"] + quantity
        total_cost = portfolio_dict[symbol]["total_cost"] + (purchase_price * quantity)
        portfolio_dict[symbol] = {"quantity": total_quantity, "total_cost": total_cost}
    else:
        portfolio_dict[symbol] = {"quantity": quantity, "total_cost": purchase_price * quantity}
    print(f"{quantity} shares of {symbol} added to your portfolio.")


# Removing stock from portfolio

def remove_stock_from_portfolio(symbol, quantity):
    symbol = symbol.upper()
    if symbol in portfolio_dict: # checking if symbol is present in portfolio are not
        if portfolio_dict[symbol]["quantity"] >= quantity:
            portfolio_dict[symbol]["quantity"] -= quantity
            if portfolio_dict[symbol]["quantity"] == 0:
                del portfolio_dict[symbol]
            print(f"Removed {quantity} shares of {symbol} from your portfolio.")
        else: 
            print(f"Insufficient quantity of {symbol} in your portfolio.")
    else:
        print(f"{symbol} not found in your portfolio.")

# Display portfolio details
def display_portfolio():
    if not portfolio_dict:
        print("Portfolio is empty...")
        return

    table = PrettyTable() # creating table for displaying portfolio details
    table.field_names = ["Stock", "Quantity", "Purchase Price", "Current Price", "Profit/Loss"] # table headers
    total_investment = 0 # initializing total investment to 0 
    total_current_value = 0 # initializing total current value to 0

    for symbol, details in portfolio_dict.items(): # iterating through portfolio dictionary
        current_price = fetch_stock_price(symbol)
        if current_price is None:
            continue
        
# getting quantity, total_cost, average_price, current_value, profit_loss of stock
        quantity = details["quantity"] 
        total_cost = details["total_cost"]
        average_price = total_cost / quantity
        current_value = quantity * current_price
        profit_loss = current_value - total_cost

        total_investment += total_cost
        total_current_value += current_value

        table.add_row([symbol, quantity, f"${average_price:.2f}", f"${current_price:.2f}", f"${profit_loss:.2f}"])

    print(table)
    print(f"Total Investment: ${total_investment:.2f}")
    print(f"Total Current Value: ${total_current_value:.2f}")
    print(f"Overall Profit/Loss: ${total_current_value - total_investment:.2f}")


# Main function to run the program
def main():
    while True: #menu loop to display to user
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Exit")
        
        try: # to catch invalid input
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        if choice == 1: # to add stock to portfolio
            symbol = input("Enter stock symbol (e.g., AAPL): ").upper()
            
            try:# to catch invalid input
                quantity = int(input(f"Enter quantity for {symbol}: "))
                purchase_price = float(input(f"Enter purchase price for {symbol}: "))
                add_stock_to_portfolio(symbol, quantity, purchase_price)
            except ValueError:
                print("Invalid input. Please enter numeric values.")
                
        elif choice == 2: # to remove stock from portfolio
            symbol = input("Enter stock symbol to remove: ").upper()
            try:
                quantity = int(input(f"Enter quantity to remove from {symbol}: "))
                remove_stock_from_portfolio(symbol, quantity)
            except ValueError:
                print("Invalid input. Please enter a numeric quantity.")
                
        elif choice == 3:# to view portfolio to user in table
            display_portfolio()
            
        elif choice == 4: # to exit the program
            print("Exiting the program. Goodbye!....")
            break
        else:
            print("Invalid choice. Please enter valid choice, try again.")



if __name__ == "__main__": # to run the program
    main()

