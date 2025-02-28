import streamlit as st
import numpy as np
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
def format_to_crores(number):
    crore_value = number / 10**7  # 1 crore = 10 million (10^7)
    return f"{crore_value:,.2f} Cr"
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
        st.header(":red[Summary]")
        st.write(stock.info.get('longBusinessSummary'))
        st.divider()
        with st.expander("Overview"):
            col1, col2 = st.columns(2)
            with col1:
                employee_count = stock.info.get('fullTimeEmployees')

                # Create a pie chart
                fig = go.Figure(data=[go.Pie(
                    labels=['Employees'],
                    values=[employee_count],
                    textinfo='label+value',
                    textfont_size=20,
                    marker=dict(colors=['pink']) 
                )])
                fig.update_layout(
                title_text='Employee Count',
                width=200,  # Set the width
                height=300,
                showlegend=False)
                
                st.subheader(f"Employee count: {employee_count}")
                st.plotly_chart(fig)

                
            with col2:
                st.write("Fiscal Year Ends")
                st.subheader("March 31")
                st.subheader(stock.info.get('industry'))
        st.link_button(
            label="Website",
            url=stock.info.get("website"),
            type="primary"
        )
        officers, mar_cap, emp_count = st.columns([2, 1, 1], gap="small")

        # Officers
        #st.write(data.info.get('companyOfficers'))
        with officers:
            st.subheader(":rainbow[Officers]")
            off1, off2 = st.columns([1, 1], gap="small")
            officers = stock.info.get('companyOfficers', 'No Data')
            with off1:
                with st.popover(label=officers[0]['title'], icon=":material/badge:"):
                    st.metric(label=officers[0]['title'], value=officers[0]['name'])

            with off2:
                with st.popover(label=officers[1]['title'], icon=":material/badge:"):
                    st.metric(label=officers[1]['title'], value=officers[1]['name'])
        
        # Market Capital
        with mar_cap:
            st.subheader(":rainbow[Market Capital]")
           
            st.metric(label="Market Cap", value=format_to_crores(stock.info.get('marketCap', 'No Data')), label_visibility="collapsed")
                
        # Sector and Industry

        st.subheader(":rainbow[Sector & Industry]")
        emp1, sector, industry, emp2 = st.columns([0.1, 2, 2, 0.1], gap="medium")
        with sector:
            st.metric(label="Sector", value=stock.info.get('sector', 'No Data'), border=True)
        with industry:
            st.metric(label="Industry", value=stock.info.get('industry', 'No Data'), border=True)
        
        st.divider()

        st.subheader(":rainbow[Location]")
        col1, col2, col3 = st.columns([2, 1, 1])

        # Display information in columns
        col1.metric(label="Address", value=stock.info.get("address1"),border=False)

    
        col2.metric(label="City",value=stock.info.get("city"))

       
        col3.metric(label="Country",value = stock.info.get("country"))


    elif selected_option == "News":
        st.header(":red[News]")
        news = stock.news
        # st.write(news[0]['content'].keys())
        for i in range(len(news)):
            data = news[i]['content']
            st.subheader(data['title'])
            with st.expander("Read More"):
                st.write(data['summary'])
    elif selected_option == "Profile":
        st.header(":red[Profile]")
        df_officers = pd.DataFrame(stock.info.get('companyOfficers'))
        st.dataframe(df_officers[['name', 'title']], width=1080)

    elif selected_option == "Analysis":
        st.header(":red[Analysis]")
        stock_price = stock.analyst_price_targets
        labels = list(stock_price.keys())
        values = list(stock_price.values())

        bar_prices = go.Figure(data=[go.Bar(x=labels, y=values)])
        bar_prices.update_layout(title='Stock Data', xaxis_title='Metric', yaxis_title='Value')
        st.plotly_chart(bar_prices)

        # Earnings Estimate
        st.header(":red[Earnings Estimate]")
        earning_estimates = stock.earnings_estimate
        earning_estimates.rename(index={'0q': "Curr Qtr", "+1q": "Next Qtr", "0y": "Curr Year", "+1y": "Next Year"}, inplace=True)
        st.write(earning_estimates.T)

        # Revenue Estimate
        st.header(":red[Revenue Estimate]")
        revenue_est = stock.revenue_estimate
        revenue_est.rename(index={'0q': "Curr Qtr", "+1q": "Next Qtr", "0y": "Curr Year", "+1y": "Next Year"}, inplace=True)
        st.write(revenue_est.T)

        # EPS Trend
        st.header(":red[EPS Trend]")
        eps = stock.eps_trend
        eps.rename(index={'0q': "Curr Qtr", "+1q": "Next Qtr", "0y": "Curr Year", "+1y": "Next Year"}, inplace=True)
        st.write(eps)

        # Growth Estimates
        st.header(":red[Growth Estimate]")
        gs = stock.growth_estimates
        gs.rename(index={'0q': "Curr Qtr", "+1q": "Next Qtr", "0y": "Curr Year", "+1y": "Next Year"}, inplace=True)
        st.write(gs.T)

    elif selected_option == "Chart":
        yf_periods = {"5D": "5d", "1M": "1mo", "6M": "6mo", "YTD": "ytd", "1Y": "1y", "5Y": "5y", "All": "max"}

        df_history = stock.history(period="1mo").reset_index()
        df_history.drop(["Dividends", "Stock Splits"], axis=1, inplace=True)
        st.header(stock.info.get('shortName', 'Stock'))

        with st.container():
            time_frame = som.option_menu(menu_title=None, options=list(yf_periods.keys()), orientation="horizontal")
            st.session_state['time_frame'] = time_frame

        st.write(stock.history(period=yf_periods[time_frame]))
        prices=stock.history(period=yf_periods[time_frame]).reset_index()
        


        with st.container(border=True):
            st.header(":red[Charts]")
        
        
            st.line_chart(prices, x="Date", y="Close", color="#ff00f0")
            st.divider()
        line_chart, candlestick = st.tabs(['Line Chart', 'Candlestick'])


        # Line Chart
        with line_chart:
            # st.subheader(f"Line Chart for {time_frames}")
            line_chart = px.line(data_frame=prices, x="Date", y="Close")
            st.plotly_chart(line_chart, theme="streamlit")
        
        # Candlestick Chart
        with candlestick:
            # st.subheader(f"Candlestick Chart for {time_frames}")
            candlestick_chart = go.Figure(data=[go.Candlestick(x=prices['Date'],
                    open=prices['Open'],
                    high=prices['High'],
                    low=prices['Low'],
                    close=prices['Close'],
                    increasing_line_color= 'cyan', decreasing_line_color= 'gray')])
            candlestick_chart.update_layout(xaxis_rangeslider_visible=False)
            st.plotly_chart(candlestick_chart, theme="streamlit")
        


           
            


