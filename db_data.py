from sqlalchemy import Column, Integer, Text, String, DateTime, Float, Numeric
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



# engine = create_engine('postgresql://postgres:password@localhost:5432/postgres', echo = True)
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


def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
