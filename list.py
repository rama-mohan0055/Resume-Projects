import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Step 1: Fetch Indian Stock Names
stocks = {
    'RELIANCE': 'RELIANCE.NS',
    'TCS': 'TCS.NS',
    'INFY': 'INFY.NS',
    'HDFCBANK': 'HDFCBANK.NS',
    'ICICIBANK': 'ICICIBANK.NS'
}

# Convert to DataFrame and save to CSV
stocks_df = pd.DataFrame(list(stocks.items()), columns=['Stock Name', 'Ticker'])
stocks_df.to_csv('indian_stocks.csv', index=False)

# Step 2: Streamlit App
st.title('Indian Stocks Selector')

# Load the CSV file
stock_data = pd.read_csv('indian_stocks.csv')

# Selectbox for stock names
selected_stock = st.selectbox('Select a Stock:', stock_data['Stock Name'])

# Display selected stock ticker
ticker = stock_data[stock_data['Stock Name'] == selected_stock]['Ticker'].values[0]
st.write(f'Selected Stock Ticker: {ticker}')

# Step 3: Fetch Open Prices for the Last Month
stock_info = yf.Ticker(ticker)
history = stock_info.history(period='1mo')

# Store Open prices in a dictionary
open_prices = history['Open'].to_dict()

# Display dictionary
st.write('Open Prices for the Last Month:', open_prices)

# Step 4: Plot Line Graph
st.line_chart(history['Open'])
