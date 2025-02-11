import yfinance as yf
df = yf.download('ZOMATO.NS', start='2021-01-01', end='2023-02-25')
print(df.head())
print(df.shape)