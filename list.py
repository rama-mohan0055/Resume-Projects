import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
# Step 1: Fetch Indian Stock Names
ticker = yf.Ticker('TCS.NS')

incomestmt = ticker.income_stmt

dates = list(incomestmt.columns)

formatted_dates = pd.to_datetime(dates).strftime('%Y')

st.write(formatted_dates)

incomestmt = incomestmt.T

incomestmt["Dates"] = formatted_dates

st.write(incomestmt)

total_rev, net_income = st.columns(2)

with total_rev:
    bar_chart = px.bar(incomestmt, x=formatted_dates, y="Total Revenue",
                title="Total Revenue",
                text_auto=True)

    st.plotly_chart(bar_chart, theme="streamlit")
