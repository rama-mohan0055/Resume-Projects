import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
import datetime as dt

df=pd.read_csv("filtered_nifty_50.csv")

st.set_page_config("Ram Mohan", layout="wide")
st.title("stock market")

st.sidebar.title("Navigation")
selected_option = st.sidebar.radio("Select an option:", ["Summary", "News","Profile", "Analysis", "Chart"])

stocknames=df['NAME OF COMPANY'].to_list()
col1,col2=st.columns([2,2])
with col1:
    data=st.selectbox(label="selectstock", options= stocknames,label_visibility="collapsed")
with col2:
    download=st.button("DOWNLOAD")

symbol = df.loc[df["NAME OF COMPANY"]==data,'SYMBOL'].values[0]+".NS"
stock = yf.Ticker(symbol)

if selected_option=="Summary":
    st.header("Summary")
    st.write(stock.info.get('longBusinessSummary'))
    st.divider()
    with st.expander("Overview"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"Employee count is \n{stock.info.get('fullTimeEmployees')}")
            st.subheader(stock.info.get('sector'))
        with col2:
            st.write("Fiscal Year Ends")
            st.subheader("March 31")
            st.subheader(stock.info.get('industry'))
        st.write(stock.info.get("website"))
    st.write(stock.info['address1'])
    st.write(stock.info['city'])
    st.write(stock.info['country'])

elif selected_option=="News":
    st.header("News")
    news = stock.news
    #st.write(news)

    for article in news:
        data=article['content']
        #st.write(data.keys())

        title = data['title']
        st.subheader(title)
        with st.expander("See explanation"):
            st.write(data["summary"])
elif selected_option=="Profile":
    df = pd.DataFrame(stock.info.get('companyOfficers'))
    #st.dataframe(df)
    st.dataframe(df[['name', 'title']], width=1080)
                
elif selected_option=="Analysis":
    st.header("Analysis")
    st.write(stock.analyst_price_targets)
    



else:
    st.header("charts")
    
    if download:
       
        stockname=stock.info.get('shortName',)
        

        df = stock.history(period="1mo")
        df = df.reset_index()
        st.header(stockname)

        df.drop(["Dividends","Stock Splits"],axis=1,inplace=True)
        st.write(df.tail())
        st.write(df.columns)
        col1, col2 = st.columns([1,1])

        with col1:
            
            
            st.line_chart(df, x="Date", y="Close",color="#ff00f0")
            st.area_chart(df,x="Date", y="Volume",color="#ff00ff")
            st.divider()
        with col2:
            st.bar_chart(df, x="Date", y="Volume")
            st.scatter_chart(df, x="Date",y="High",color=["#FF0000"])
            fig = px.bar(df, x='Date', y='Volume')
            st.plotly_chart(fig)       
            






