timeframes = {
"1D": "1d",
"5D": "5d",
"1M": "1mo",
"6M": "6mo",
"YTD": f"{dt.datetime.now().year}-01-01",
"1Y": "1y",
"5Y": "5y",
"All": None}

selected_timeframe = st.selectbox("Select Timeframe", list(timeframes.keys()))
if selected_timeframe:
    if selected_timeframe == "All":
        data = yf.download(stocknames)
    else:
        period = timeframes[selected_timeframe]
        if period == "1d":
            data = yf.download(stocknames, period=period, interval="1m")
        else:
            data = yf.download(stocknames, period=period)

        st.subheader(f"Data for {stocknames} over {selected_timeframe}")
        st.line_chart(data['Close'])

        st.write(data)