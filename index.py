import streamlit as st

st.set_page_config("Ram Mohan", layout="wide")
st.title("stock market")
stockname=["ZOMATO.NS"]
st.selectbox(label="selectstock", options= stockname)
download=st.button("DOWNLOAD")
if download:
    import yfinance as yf
    stock = yf.Ticker("ZOMATO.NS")
    df = stock.history(period="1mo", interval="1d")
    df = df.reset_index()
    st.write(df.head())
    st.write(df.columns)
    col1, col2 = st.columns([1,2])
    with col1:
        st.line_chart(df, x="Date", y="Close")
        st.divider()
    with col2:
        st.bar_chart(df, x="Date", y="Volume")





