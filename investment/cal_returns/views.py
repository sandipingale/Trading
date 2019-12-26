from django.shortcuts import render
import sys
from datetime import date
from .forms import StockForm, InvStockForm, SectReturnForm
xxpath = "C:\\Users\\lenovo\\PycharmProjects\\Trading"
sys.path.append(xxpath)
from xirr import xirr
from query_stocks import get_results, inv_test


def getxirr(request):
    tas = [(date(2006, 1, 24), -39967),
           (date(2008, 2, 6), -19866),
           (date(2010, 10, 18), 245706),
           (date(2013, 9, 14), 52142)]
    print("IRR for test data = {:.2%}".format(xirr(tas)))
    return render(request, 'cal_returns/xirr.html', {'xirr': "{:.2%}".format(xirr(tas))})


def stock_details(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol_name']
            series = form.cleaned_data['series']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            data, min_val, max_val = get_results(symbol, series, start_date, end_date)
            return render(request, 'cal_returns/stock_details.html', {'form': form,
                                                                      'data': data,
                                                                      'min': min_val,
                                                                      'max': max_val})
    else:
        form = StockForm()
        return render(request, 'cal_returns/stock_details.html', {'form': form})


def inv_return_test(request):
    if request.method == 'POST':
        form = InvStockForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol_name']
            series = form.cleaned_data['series']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            no_of_shares = form.cleaned_data['no_of_shares']
            multiply = form.cleaned_data['multiply']
            moving_average = form.cleaned_data['moving_average']

            data, xirr_value, inv_to_proceed, tot_inv, tot_ret = inv_test(symbol, series, start_date, end_date,
                                                                          no_of_shares, multiply, moving_average)
            abs_ret = (tot_ret - tot_inv)/tot_inv * 100
            return render(request, 'cal_returns/inv_return_test.html', {'form': form,
                                                                        'data': data,
                                                                        'xirr': xirr_value,
                                                                        'inv_to_proceed': inv_to_proceed,
                                                                        'total_inv': tot_inv,
                                                                        'total_ret': tot_ret,
                                                                        'abs_return': abs_ret})
    else:
        form = InvStockForm()
        return render(request, 'cal_returns/inv_return_test.html', {'form': form})

def home(request):
    return render(request,'cal_returns/home.html')


def sect_return(request):
    if request.method == 'POST':
        form = SectReturnForm(request.POST)
        if form.is_valid():
            sector = form.cleaned_data['sector']
            series = form.cleaned_data['series']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            no_of_shares = form.cleaned_data['no_of_shares']
            multiply = form.cleaned_data['multiply']
            moving_average = form.cleaned_data['moving_average']
            symbols = []
            if sector == 'IT':
                symbols = ['WIPRO', 'TCS', 'INFY', 'TECHM', 'NIITTECH', 'HCLTECH', 'TATAELXSI', 'MINDTREE', 'HEXAWARE',
                       ]
            if sector == 'Auto':
                symbols = ['ASHOKLEY', 'HEROMOTOCO', 'M&M', 'APOLLOTYRE', 'MRF', 'BAJAJ-AUTO', 'MARUTI', 'EICHERMOT',
                           'MOTHERSUMI', 'TVSMOTOR', 'TATAMOTORS', 'BOSCHLTD', 'EXIDEIND', 'AMARAJABAT', 'BHARATFORG']
            if sector == 'Bank':
                symbols = ['IDFCFIRSTB', 'INDUSINDBK', 'YESBANK', 'SBIN', 'AXISBANK', 'PNB', 'HDFCBANK', 'BANKBARODA',
                           'RBLBANK', 'ICICIBANK', 'KOTAKBANK', 'FEDERALBNK']
            if sector == 'ETF':
                symbols = ['NIFTYBEES', 'KOTAKBKETF', 'CPSEETF', 'SETFNIFBK', 'SETFNIF50', 'BANKBEES', 'ICICINIFTY',
                           'GOLDBEES', 'ICICILIQ']
            if len(symbols) == 0:
                symbols = ['NIFTYBEES']
            sect_ret_results = []
            for symbol in symbols:
                data, xirr_value, inv_to_proceed, tot_inv, tot_ret = inv_test(symbol, series, start_date, end_date,
                                                                              no_of_shares, multiply, moving_average)
                sect_ret_results.append((symbol, xirr_value, inv_to_proceed, data[-1][0], data[-1][1]))
            return render(request, 'cal_returns/sect_return.html', {'form': form,
                                                                    'data': sect_ret_results,
                                                                    })
    else:
        form = SectReturnForm()
        return render(request, 'cal_returns/sect_return.html', {'form': form})
