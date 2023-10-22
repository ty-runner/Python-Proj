from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests

url = "https://www.smartinsider.com/politicians/"
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Locate the section containing recent trades
    recent_trades_section = soup.find('section', {'class': 'recent-trades'})
    
    if recent_trades_section:
        # Extract the relevant data
        trade_items = recent_trades_section.find_all('div', {'class': 'trade-item'})
        
        for trade_item in trade_items:
            # Extract and print the trade information
            trade_date = trade_item.find('div', {'class': 'trade-date'}).text.strip()
            trade_description = trade_item.find('div', {'class': 'trade-description'}).text.strip()
            trade_type = trade_item.find('div', {'class': 'trade-type'}).text.strip()
            trade_amount = trade_item.find('div', {'class': 'trade-amount'}).text.strip()
            
            print(f"Date: {trade_date}")
            print(f"Description: {trade_description}")
            print(f"Type: {trade_type}")
            print(f"Amount: {trade_amount}")
            print('-' * 40)
    else:
        print("Recent trades section not found on the page.")
else:
    print("Failed to retrieve the page. Status code:", response.status_code)
