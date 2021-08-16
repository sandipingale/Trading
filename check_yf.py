import yfinance as yf

symbol = yf.Ticker("TCS.NS")

# get stock info
#print(symbol.info)

# get historical market data
hist = symbol.history(period="1mo")
hist = hist.reset_index()
hist['just_date'] = hist['Date'].dt.date
for index, row in hist.iterrows():
    print(row['Close'],type(row['just_date']))

