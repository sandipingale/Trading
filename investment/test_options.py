import yfinance as yf

nifty = yf.Ticker("^NSEI")
print(nifty.info)
ops = nifty.option_chain('2021-08-12')
print(ops)
