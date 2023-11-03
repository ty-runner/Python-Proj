from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests

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
df.to_csv(csv_file_path, index=False)
grouped_trades = df.groupby('Senator').sum()
print(grouped_trades)
for senator, group in grouped_trades.groupby('Senator'):
    print(f"{senator}: {group['Amount'].sum()}")
for index, row in df.iterrows():
    print(f"{index}: {row['Stock']} - {row['Date Disclosed']} - {row['Senator']} - {row['Action']} - {row['Type']} - {row['Amount']}")

