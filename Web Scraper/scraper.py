from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go
import requests
import matplotlib.pyplot as plt
from flask import Flask, render_template
from io import BytesIO
import base64

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
        amount = columns[5].text.strip().replace('$', '').replace(',', '')
        if '-' in amount:
            lower, upper = map(float, amount.split('-'))
            amount = (lower + upper) / 2
        else:
            amount = float(amount)

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
stock_stats = df.groupby('Stock').agg({
    'Amount': 'sum',    # Total amount traded
})
app = Flask(__name__)

@app.route('/')
def index():
    # Generate plots
    senator_stats_plot = generate_bar_chart(senator_stats, 'Number of Stock Transactions by Senator', 'Senator', 'Number of Transactions')

    # Convert plots to HTML format
    senator_stats_plot_html = plot_to_html(senator_stats_plot)
    stock_stats_plot = generate_bar_chart(stock_stats, 'Total Amount Traded by Stock Symbol', 'Stock Symbol', 'Total Amount Traded')
    stock_stats_plot_html = plot_to_html(stock_stats_plot)

    # Render the HTML template with the plots
    return render_template('index.html', senator_stats_plot=senator_stats_plot_html, stock_stats_plot=stock_stats_plot_html)

def generate_bar_chart(data, title, xlabel, ylabel):
    plt.figure(figsize=(2, 8))
    data.plot(kind='bar')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=15)
    return plt

def plot_to_html(plot):
    img = BytesIO()
    plot.savefig(img, format='png', dpi=100)
    img.seek(0)
    plot_data = base64.b64encode(img.getvalue()).decode()
    return f'<img src="data:image/png;base64, {plot_data}" alt="plot">'

if __name__ == '__main__':
    app.run(debug=True)