import streamlit as st
import yfinance as yf

st.set_page_config("Ram Mohan", layout="wide")
st.title("stock market")
stockname=["ZOMATO.NS","INFY.NS"]
col1,col2=st.columns([2,2])
with col1:
    data=st.selectbox(label="selectstock", options= stockname,label_visibility="collapsed")
with col2:
    download=st.button("DOWNLOAD")
if download:
    stock = yf.Ticker(data)
    stockname=stock.info.get('shortName')

    df = stock.history(period="1mo")
    df = df.reset_index()
    st.header(stockname)
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






