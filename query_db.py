from sqlalchemy import Column, String, DateTime, Float, Numeric
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import datetime
from investment.cal_returns.services.xirr import xirr

#engine = create_engine('postgresql://postgres:password@localhost:5432/postgres', echo = True)
engine = create_engine('postgresql://postgres:password@localhost:5432/postgres')
Base = declarative_base()

class Stocks(Base):
    __tablename__ = 'stocks'
    symbol = Column(String, primary_key=True)
    series = Column(String, primary_key=True)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    last_price = Column(Float)
    prev_close = Column(Float)
    tot_trd_qty = Column(Numeric)
    tot_trd_value = Column(Float)
    txn_date = Column(DateTime, primary_key=True)
    isin_number = Column(String)
    unnamed = Column(String)


Session = sessionmaker(bind = engine)
session = Session()
result = session.query(Stocks).filter(Stocks.symbol == 'TCS', Stocks.series == 'EQ', Stocks.txn_date > '2016-01-01')


df = pd.DataFrame([(d.symbol, d.txn_date.date(), d.close_price) for d in result],
                  columns=['symbol', 'txn_date', 'close_price'])
df = df.sort_values(by='txn_date')
df['MA'] = df['close_price'].rolling(window=10).mean()
df['avg_diff'] = (df['close_price'] - df['MA'])/df['MA']*100
df['inv_value'] = df['close_price']  * -5
#print(df)
print(df[df['avg_diff']<0].mean(axis=0)['avg_diff'])
session.close()
inv = df[df['avg_diff'] < df[df['avg_diff']<0].mean(axis=0)['avg_diff']*1.2]
print(inv[['txn_date','close_price']])
inv_list = list(inv[['txn_date','inv_value']].to_records(index=False))
shares = len(inv_list) * 5
inv_list.append((datetime.date(2019,10,3), 2200*shares))
print (inv_list)
print("IRR for test data = {:.2%}".format(xirr(inv_list)))