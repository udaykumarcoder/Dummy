import time
import yfinance as yf
from plyer import notification

# Define the stock symbol
symbol = 'RITES.NS'  # Replace with the desired stock symbol

def fetch_opening_price_and_52_week_high(symbol):
    # Create a Ticker object
    stock = yf.Ticker(symbol)

    # Fetch historical data for the past year
    historical_data = stock.history(period='1y')

    # Check if historical data is empty
    if historical_data.empty:
        print("No historical data found.")
        return None, None

    # Calculate the 52-week high
    fifty_two_week_high = historical_data['High'].max()

    # Fetch the latest day's data for the opening price
    latest_data = stock.history(period='1d')

    # Check if the latest day's data is empty
    if latest_data.empty:
        print("No latest data found.")
        return None, fifty_two_week_high

    # Get the opening price for the latest trading day
    opening_price = latest_data['Open'].iloc[0]

    return opening_price, fifty_two_week_high

def fetch_current_price(symbol):
    # Fetch current stock data
    stock = yf.Ticker(symbol)
    current_data = stock.history(period="1d", interval="1m")  # Fetch recent 1-minute interval data
    
    if current_data.empty:
        print("Failed to retrieve current price.")
        return None

    # Get the last price from recent data
    current_price = current_data['Close'].iloc[-1]
    return current_price

def alert_user(message):
    notification.notify(
        title="Stock Alert",
        message=message,
        app_name="Stock Alert System",
        timeout=10  # Notification duration
    )

# Get the opening price and 52-week high
opening_price, fifty_two_week_high = fetch_opening_price_and_52_week_high(symbol)

if opening_price is not None and fifty_two_week_high is not None:
    print(f"Opening Price of {symbol}: {opening_price}")
    print(f"52-Week High of {symbol}: {fifty_two_week_high}")

    # Flags to track notifications
    notified_target = False
    notified_high = False

    # Continuously check the stock price
    while True:
        # Fetch the current stock price
        current_price = fetch_current_price(symbol)
        target = 389

        if current_price is None:
            print("Failed to retrieve current price, retrying...")
        else:
            print(f"Current Price: {current_price}")

            # Check if the current price hits or exceeds the target
            if current_price >= target and not notified_target:
                alert_user(f"{symbol} has reached the target price of {target}. Current Price: {current_price}")
                notified_target = True  # Set the flag to indicate the notification has been sent

            # Check if the current price hits or exceeds the 52-week high
            if current_price >= fifty_two_week_high and not notified_high:
                alert_user(f"{symbol} has hit its 52-week high of {fifty_two_week_high}! Current Price: {current_price}")
                notified_high = True  # Set the flag to indicate the notification has been sent
        
        # Wait before checking again (e.g., 10 seconds for a faster refresh)
        time.sleep(10)
else:
    print("Failed to retrieve opening price or 52-week high.")
