#from db_data import Stocks, get_session
from datetime import date
import pandas as pd
from .xirr import xirr
import yfinance as yf

def get_results(symbol='symbol', series='series', start_date=date.today(), end_date=date.today()):
#    session = get_session()
#    result_tmp = session.query(Stocks).filter(Stocks.symbol == symbol, Stocks.series == series, Stocks.txn_date >
#                                              start_date, Stocks.txn_date < end_date)
#    data = []
#    max_list = []
#    for row in result_tmp:
#        data.append((row.symbol, row.series, row.txn_date, row.close_price))
#        max_list.append(row.close_price)
#    session.close()
#    return data, min(max_list), max(max_list)
    data = []
    max_list = []
    tick = yf.Ticker(symbol)
    hist = tick.history(start=start_date, end=end_date)
    hist = hist.reset_index()
    for index, row in hist.iterrows():
        data.append((symbol,series,row['Date'],row['Close']))
        max_list.append(row['Close'])
    return data, min(max_list), max(max_list)




#def get_results(symbol='symbol', series='series', start_date=date.today(), end_date=date.today()):
#    session = get_session()
#    result_tmp = session.query(Stocks).filter(Stocks.symbol == symbol, Stocks.series == series, Stocks.txn_date >
#                                              start_date, Stocks.txn_date < end_date)
#    data = []
#    max_list = []
#    for row in result_tmp:
#        data.append((row.symbol, row.series, row.txn_date, row.close_price))
#        max_list.append(row.close_price)
#    session.close()
#    return data, min(max_list), max(max_list)


#def inv_test(symbol='symbol', series='series', start_date=date.today(), end_date=date.today(), no_of_shares=10,
#             multiply_fact=1.4, moving_average=10):
#    session = get_session()
#    result_tmp = session.query(Stocks).filter(Stocks.symbol == symbol, Stocks.series == series, Stocks.txn_date >
#                                              start_date, Stocks.txn_date < end_date)
#    obj = session.query(Stocks).filter(Stocks.symbol == symbol, Stocks.series == series).\
#        order_by(Stocks.txn_date.desc()).first()
#    df = pd.DataFrame([(d.symbol, d.txn_date.date(), d.close_price) for d in result_tmp],
#                      columns=['symbol', 'txn_date', 'close_price'])
#    df = df.sort_values(by='txn_date')
#    df['MA'] = df['close_price'].rolling(window=moving_average).mean()
#    df['avg_diff'] = (df['close_price'] - df['MA']) / df['MA'] * 100
#    df['inv_value'] = df['close_price'] * -1 * no_of_shares
#    session.close()
#    print(df[df['avg_diff'] < 0].mean(axis=0)['avg_diff'])
#    inv_to_proceed = obj.close_price + (obj.close_price * df[df['avg_diff'] < 0].mean(axis=0)['avg_diff'] *
#                                        multiply_fact / 100)
#    inv = df[df['avg_diff'] < df[df['avg_diff'] < 0].mean(axis=0)['avg_diff'] * multiply_fact]
#    inv_list = list(inv[['txn_date', 'inv_value']].to_records(index=False))
#    shares = len(inv_list) * no_of_shares
#    inv_list.append((obj.txn_date.date(), obj.close_price * shares))
#    price_dict = {}
#    ma_dict = {}
#    for index, row in df.iterrows():
#        price_dict[row['txn_date']] = row['close_price']
#        ma_dict[row['txn_date']] = row['MA']
#    price_dict[obj.txn_date.date()] = obj.close_price
#    if obj.txn_date.date() not in ma_dict:
#        ma_dict[obj.txn_date.date()] = 0

#    inv_result = []
#    total_inv_amount = 0
#    total_return_amount = 0
#    for inv_date, inv_amount in inv_list:
#        inv_result.append((inv_date, price_dict[inv_date], ma_dict[inv_date], no_of_shares, inv_amount))
#        if inv_amount < 0:
#            total_inv_amount = total_inv_amount + inv_amount * -1
#        else:
#            total_return_amount = inv_amount
#    return inv_result, "{:.2%}".format(xirr(inv_list)), inv_to_proceed, total_inv_amount, total_return_amount


def new_inv_test(symbol='symbol', series='series', start_date=date.today(), end_date=date.today(), no_of_shares=10,
                 multiply_fact=1.4, moving_average=10):
    symbol = yf.Ticker(symbol)
    hist = symbol.history(start=start_date, end=end_date)
    df = hist
    df = df.reset_index()
    df['MA'] = df['Close'].rolling(window=moving_average).mean()
    df['avg_diff'] = (df['Close'] - df['MA']) / df['MA'] * 100
    df['inv_value'] = df['Close'] * -1 * no_of_shares
    df['just_date'] = df['Date'].dt.date
    last_rec = df.tail(1).to_dict('records')
    last_rec = last_rec[0]
    inv_to_proceed = last_rec['Close'] + (last_rec['Close'] * df[df['avg_diff'] < 0].mean(axis=0)['avg_diff'] *
                                        multiply_fact / 100)
    inv = df[df['avg_diff'] < df[df['avg_diff'] < 0].mean(axis=0)['avg_diff'] * multiply_fact]
    inv_list = list(inv[['just_date', 'inv_value']].to_records(index=False))
    shares = len(inv_list) * no_of_shares

    inv_list.append((last_rec['just_date'], last_rec['Close'] * shares))
    for tmp_dt in inv_list:
        print(type(tmp_dt[0]),tmp_dt[0],tmp_dt[1])
    price_dict = {}
    ma_dict = {}
    for index, row in df.iterrows():
        price_dict[row['Date']] = row['Close']
        ma_dict[row['Date']] = row['MA']
    price_dict[last_rec['Date']] = last_rec['Close']

    if last_rec['Date'] not in ma_dict:
        ma_dict[last_rec] = 0

    inv_result = []
    total_inv_amount = 0
    total_return_amount = 0
    for inv_date, inv_amount in inv_list:
        tmp_date = get_date(inv_date)
        inv_result.append((inv_date, price_dict[tmp_date], ma_dict[tmp_date], no_of_shares, inv_amount))
        if inv_amount < 0:
            total_inv_amount = total_inv_amount + inv_amount * -1
        else:
            total_return_amount = inv_amount
    return inv_result, "{:.2%}".format(xirr(inv_list)), inv_to_proceed, total_inv_amount, total_return_amount


def get_date(inp_date):
    return pd.to_datetime(inp_date)

if __name__ == '__main__':
    s_date = date(2021, 1, 1)
    e_date = date(2021, 8, 8)
    result, per, pos_inv, amount_invested, amount_returned = new_inv_test('INFY.NS', 'EQ', s_date, e_date, 2, 1.8)
    print(result)
    print(per,pos_inv)
