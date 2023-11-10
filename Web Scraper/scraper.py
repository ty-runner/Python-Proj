from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go
import requests
import matplotlib.pyplot as plt

url = "https://www.quiverquant.com/sources/senatetrading"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
    
    # Specify the file path where you want to save the content
file_path = "soup_content.html"  # Change this to the desired file path and name

    # Write the content of soup to the specified file
with open(file_path, "w", encoding="utf-8") as file:
        file.write(soup.prettify())
with open('soup_content.html', 'r', encoding='utf-8') as file:
    html_content = file.read()
# Check if the request was successful (status code 200)
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table with class 'senate-trading-table'
table = soup.find('table', class_='senate-trading-table')

# Initialize lists to store the scraped data
data = []

# Iterate through rows in the table
for row in table.find_all('tr'):
    columns = row.find_all('td')
    if columns:
        stock = columns[0].text.strip()
        date_disclosed = columns[1].text.strip()
        senator = columns[2].text.strip()
        purchase_sale = columns[3].text.strip()
        trade_type = columns[4].text.strip()
        amount = columns[5].text.strip()
        
        amount = amount.replace('$', '').replace(',', '')
        lower,upper = amount.split('-')
        # lower = float(lower)
        # upper = float(upper)
        # amount = (lower+upper)/2
        data.append({
            "Stock": stock,
            "Date Disclosed": date_disclosed,
            "Senator": senator,
            "Action": purchase_sale,
            "Type": trade_type,
            "Amount": amount,
        })

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(data)
csv_file_path = "senate_trading_data.csv"
#if we have duplicates, we shouldn't add them to the data, we can iterate through the csv and then take out the data that matches with the lines in the csv
df.to_csv(csv_file_path, index=False)

senator_stats = df.groupby('Senator').agg({
    'Action': 'count',  # Number of transactions
    'Amount': 'sum',    # Total amount traded
})

# Visualize the data
# For example, you can create a bar chart to show the number of transactions by senator.
senator_stats['Action'].plot(kind='bar', figsize=(10, 6))
plt.title('Number of Stock Transactions by Senator')
plt.xlabel('Senator')
plt.ylabel('Number of Transactions')
plt.xticks(rotation=15)
plt.show()

# Analyze stock transactions by stock symbol
stock_stats = df.groupby('Stock').agg({
    'Amount': 'sum',    # Total amount traded
})

# Visualize the data
# For example, you can create a bar chart to show the total amount traded by stock symbol.
stock_stats['Amount'].plot(kind='bar', figsize=(10, 6))
plt.title('Total Amount Traded by Stock Symbol')
plt.xlabel('Stock Symbol')
plt.ylabel('Total Amount Traded')
plt.xticks(rotation=0)
plt.show()