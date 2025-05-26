"""
---------------------------------------------------------------
Fetching stock data from Yahoo Stock Screener
---------------------------------------------------------------
Author: Ebelechukwu Igwagu
---------------------------------------------------------------
This script fetches stock data from Yahoo Finance and saves them to a JSON file. 
These were used to populate the stocks table in the investment portfolio management system and also 
to simulate initial prices for the transaction table.
"""

import json
import time
import requests

# Soecifies the file path to save the JSON data
file_path = r"C:\Users\great\Desktop\ATU\Year 2\Sem 1\web services and applications\WSAA-coursework\WSAA_Project/stocks.json"

# Yahoo Finance Screener Endpoint
url = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved?scrIds=most_actives&count=50"

time.sleep(2)  # Adding a delay 

try:
    # Adding headers to mimic a browser request to avoid being blocked by the server
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    # Get the data from Yahoo Finance WITH headers
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises an HTTPError if the response was an error

    data = response.json()

    # Save the data to a JSON file
    with open(file_path, "w") as st:
        json.dump(data, st, indent=4)

    #print("Stock data saved to stock_symbols.json")

except requests.RequestException as e:
    print(f"Error fetching stock data: {e}")




"""
------------
References:
------------
- Yahoo Finance Screeners (18.05.2025). https://finance.yahoo.com/research-hub/screener/.
"""