import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import datetime

# Read Data
df = pd.read_csv("filtered_nifty_50.csv")

# Page Config
st.set_page_config("Ram Mohan", layout="wide")
st.title("Stock Market")

# Stock Selection
stocknames = df['NAME OF COMPANY'].to_list()
col1, col2 = st.columns([2, 2])

with col1:
    data = st.selectbox(label="Select Stock", options=stocknames, label_visibility="collapsed")

with col2:
    download = st.button("DOWNLOAD")

if download:
    symbol = df.loc[df["NAME OF COMPANY"] == data, 'SYMBOL'].values[0] + ".NS"
    stock = yf.Ticker(symbol)
    stockname = stock.info.get('shortName')

    df = stock.history(period="1mo").reset_index()
    st.header(stockname)

    df.drop(["Dividends", "Stock Splits"], axis=1, inplace=True)
    st.write(df.tail())

    # Initialize session state for date selection
    if "selected_date" not in st.session_state:
        st.session_state.selected_date = datetime.date.today()

    with st.container():
        col1, col2 = st.columns([1, 1])

        with col1:
            # Date selection with session state
            st.session_state.selected_date = st.date_input("Select Date", st.session_state.selected_date)
            st.write("Selected Date:", st.session_state.selected_date)

            # Charts
            st.line_chart(df, x="Date", y="Close", color="#ff00f0")
            st.area_chart(df, x="Date", y="Volume", color="#ff00ff")
            st.divider()

        with col2:
            st.bar_chart(df, x="Date", y="Volume")
            st.scatter_chart(df, x="Date", y="High", color=["#FF0000"])
            fig = px.bar(df, x='Date', y='Volume')
            st.plotly_chart(fig)
