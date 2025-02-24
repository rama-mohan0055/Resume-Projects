import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit_option_menu as som

# Load the data
df = pd.read_csv("filtered_nifty_50.csv")

# Set page config
st.set_page_config("Ram Mohan", layout="wide")
st.title("Stock Market")

# Sidebar stock selection
st.sidebar.title("Navigation")
stocknames = df['NAME OF COMPANY'].to_list()
data = st.sidebar.selectbox("Select stock", stocknames)

# Download button in sidebar
if "download_clicked" not in st.session_state:
    st.session_state["download_clicked"] = False

if st.sidebar.button("DOWNLOAD"):
    st.session_state["download_clicked"] = True  # Mark download as clicked

selected_option = st.sidebar.radio("Select an option:", ["Summary", "News", "Profile", "Analysis", "Chart"])

# Fetch stock details
symbol = df.loc[df["NAME OF COMPANY"] == data, "SYMBOL"].values[0] + ".NS"
stock = yf.Ticker(symbol)

# Store in session state
st.session_state["stock"] = stock
st.session_state["symbol"] = symbol

# Ensure data is processed only after download is clicked
if st.session_state["download_clicked"]:
    
    if selected_option == "Summary":
        st.header("Summary")
        st.write(stock.info.get('longBusinessSummary'))
        st.divider()
        with st.expander("Overview"):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"Employee count: {stock.info.get('fullTimeEmployees')}")
                st.subheader(stock.info.get('sector'))
            with col2:
                st.write("Fiscal Year Ends")
                st.subheader("March 31")
                st.subheader(stock.info.get('industry'))
            st.write(stock.info.get("website"))
        st.write(stock.info.get("address1"))
        st.write(stock.info.get("city"))
        st.write(stock.info.get("country"))

    elif selected_option == "News":
        st.header("News")
        news = stock.news
        # st.write(news[0]['content'].keys())
        for i in range(len(news)):
            data = news[i]['content']
            st.subheader(data['title'])
            with st.expander("Read More"):
                st.write(data['summary'])
    elif selected_option == "Profile":
        df_officers = pd.DataFrame(stock.info.get('companyOfficers'))
        st.dataframe(df_officers[['name', 'title']], width=1080)

    elif selected_option == "Analysis":
        st.header("Analysis")
        stock_price = stock.analyst_price_targets
        labels = list(stock_price.keys())
        values = list(stock_price.values())

        bar_prices = go.Figure(data=[go.Bar(x=labels, y=values)])
        bar_prices.update_layout(title='Stock Data', xaxis_title='Metric', yaxis_title='Value')
        st.plotly_chart(bar_prices)

        # Earnings Estimate
        st.header("Earnings Estimate")
        earning_estimates = stock.earnings_estimate
        earning_estimates.rename(index={'0q': "Curr Qtr", "+1q": "Next Qtr", "0y": "Curr Year", "+1y": "Next Year"}, inplace=True)
        st.write(earning_estimates.T)

        # Revenue Estimate
        st.header("Revenue Estimate")
        revenue_est = stock.revenue_estimate
        revenue_est.rename(index={'0q': "Curr Qtr", "+1q": "Next Qtr", "0y": "Curr Year", "+1y": "Next Year"}, inplace=True)
        st.write(revenue_est.T)

        # EPS Trend
        st.header("EPS Trend")
        eps = stock.eps_trend
        eps.rename(index={'0q': "Curr Qtr", "+1q": "Next Qtr", "0y": "Curr Year", "+1y": "Next Year"}, inplace=True)
        st.write(eps)

        # Growth Estimates
        st.header("Growth Estimate")
        gs = stock.growth_estimates
        gs.rename(index={'0q': "Curr Qtr", "+1q": "Next Qtr", "0y": "Curr Year", "+1y": "Next Year"}, inplace=True)
        st.write(gs.T)

    elif selected_option == "Chart":
        yf_periods = {"1D": "1d", "5D": "5d", "1M": "1mo", "6M": "6mo", "YTD": "ytd", "1Y": "1y", "5Y": "5y", "All": "max"}

        df_history = stock.history(period="1mo").reset_index()
        df_history.drop(["Dividends", "Stock Splits"], axis=1, inplace=True)
        st.header(stock.info.get('shortName', 'Stock'))

        with st.container():
            time_frame = som.option_menu(menu_title=None, options=list(yf_periods.keys()), orientation="horizontal")
            st.session_state['time_frame'] = time_frame

        st.write(stock.history(period=yf_periods[time_frame]))

        col1, col2 = st.columns([1, 1])
        with col1:
            st.header("Charts")
            st.line_chart(df_history, x="Date", y="Close", color="#ff00f0")
            st.area_chart(df_history, x="Date", y="Volume", color="#ff00ff")
            st.divider()
        with col2:
            st.scatter_chart(df_history, x="Date", y="High", color=["#FF0000"])
            fig = px.bar(df_history, x='Date', y='Volume')
            st.plotly_chart(fig)
