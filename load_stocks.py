import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text, String, DateTime, Float, Numeric
from io import BytesIO
from zipfile import ZipFile
import pandas
import requests
import datetime
import psycopg2


def load_daily_rates(url_name='url_name'):
    url = url_name
    engine = create_engine('postgresql://postgres:password@localhost:5432/postgres')
    content = requests.get(url)
    zf = ZipFile(BytesIO(content.content))
    # find the first matching csv file in the zip:
    match = [s for s in zf.namelist() if ".csv" in s][0]
    # the first line of the file contains a string - that line shall de     ignored, hence skiprows
    df = pandas.read_csv(zf.open(match), low_memory=False, skiprows=[0])
    if len(df.columns) == 14:
        df.columns = ['symbol', 'series', 'open_price', 'high_price', 'low_price', 'close_price', 'last_price', 'prev_close',
                      'tot_trd_qty', 'tot_trd_value', 'txn_date', 'total_trades', 'isin_number', 'unnamed']
    else:
        df['unnamed'] = ''
        df.columns = ['symbol', 'series', 'open_price', 'high_price', 'low_price', 'close_price', 'last_price', 'prev_close',
                      'tot_trd_qty', 'tot_trd_value', 'txn_date', 'total_trades', 'isin_number', 'unnamed']

    df.to_sql(name='stocks', con=engine, if_exists='append', index=False, dtype={"symbol": String,
                                                                                  "series": String,
                                                                                  "open_price": Float,
                                                                                  "high_price": Float,
                                                                                  "low_price": Float,
                                                                                  "close_price": Float,
                                                                                  "last_price": Float,
                                                                                  "prev_close": Float,
                                                                                  "tot_trd_qty": Numeric,
                                                                                  "tot_trd_value": Float,
                                                                                    "txn_date": DateTime,
                                                                                  "total_trades": Numeric,
                                                                                  "isin_number": String,
                                                                                  "unnamed": String})


conn = psycopg2.connect(host="localhost",database="postgres", user="postgres", password="password")
cur = conn.cursor()
base = datetime.datetime.today()
date_list = [base - datetime.timedelta(days=x) for x in range(30)]
cur.execute('SELECT distinct txn_date as rec_date from stocks')
rows = cur.fetchall()
db_date_list = []
for row in rows:
    db_date_list.append(row[0].date())
conn.close()
for csv_date in date_list:
    if csv_date.date() in db_date_list:
         continue
    website = "https://www.nseindia.com/content/historical/EQUITIES/" + csv_date.strftime("%Y") + "/" + \
          csv_date.strftime("%b").upper() + "/" + "cm" + csv_date.strftime("%d") + \
          csv_date.strftime("%b").upper() + csv_date.strftime("%Y") + "bhav.csv.zip"
    request = requests.get(website)
    if request.status_code == 200:
        print('Web site exists')
        load_daily_rates(website)
    else:
        pass
