from django.shortcuts import render, get_object_or_404
import sys
from datetime import date
from .forms import StockForm, InvStockForm, SectReturnForm
from .services.query_stocks import  new_inv_test,get_results
from django.http import JsonResponse
import os
sys.path.append(os.path.abspath('.'))
from shares.models import ShareList




def stock_details(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol_name']
#            series = form.cleaned_data['series']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            data, min_val, max_val = get_results(symbol, 'EQ', start_date, end_date)
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
            symbol_temp = ""
            if ShareList.objects.filter(id=symbol).exists():
                symbol_obj = get_object_or_404(ShareList,id=symbol)
                symbol_temp = symbol_obj.text
            elif ShareList.objects.filter(text=symbol).exists():
                symbol_temp =  symbol
            symbol = symbol_temp
            #symbol = form.cleaned_data['symbol_name']
#           series = form.cleaned_data['series']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            no_of_shares = form.cleaned_data['no_of_shares']
            multiply = form.cleaned_data['multiply']
            moving_average = form.cleaned_data['moving_average']

            data, xirr_value, inv_to_proceed, tot_inv, tot_ret = new_inv_test(symbol, 'EQ', start_date, end_date,
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

#def home(request):
#    return render(request,'cal_returns/home.html')


def sect_return(request):
    if request.method == 'POST':
        form = SectReturnForm(request.POST)
        if form.is_valid():
            sector = form.cleaned_data['sector']
#            series = form.cleaned_data['series']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            no_of_shares = form.cleaned_data['no_of_shares']
            multiply = form.cleaned_data['multiply']
            moving_average = form.cleaned_data['moving_average']
            symbols = []
            if sector == 'IT':
                symbols = ['WIPRO.NS', 'TCS.NS', 'INFY.NS', 'TECHM.NS', 'NIITLTD.NS', 'HCLTECH.NS', 'TATAELXSI.NS', 'MINDTREE.NS', ]
            if sector == 'Auto':
                symbols = ['ASHOKLEY', 'HEROMOTOCO', 'M&M', 'APOLLOTYRE', 'MRF', 'BAJAJ-AUTO', 'MARUTI', 'EICHERMOT',
                           'MOTHERSUMI', 'TVSMOTOR', 'TATAMOTORS', 'BOSCHLTD', 'EXIDEIND', 'AMARAJABAT', 'BHARATFORG']
            if sector == 'Bank':
                symbols = ['IDFCFIRSTB', 'INDUSINDBK', 'YESBANK', 'SBIN', 'AXISBANK', 'PNB', 'HDFCBANK', 'BANKBARODA',
                           'RBLBANK', 'ICICIBANK', 'KOTAKBANK', 'FEDERALBNK']
            if sector == 'ETF':
                symbols = ['NIFTYBEES', 'KOTAKBKETF', 'CPSEETF', 'SETFNIFBK', 'SETFNIF50', 'BANKBEES', 'ICICINIFTY',
                           'GOLDBEES', 'ICICILIQ']
            if sector == 'NIFTY50':
                symbols = [
                    'ADANIPORTS.NS',
                    'ASIANPAINT.NS',
                    'AXISBANK.NS',
                    'BAJAJ-AUTO.NS',
                    'BAJFINANCE.NS',
                    'BAJAJFINSV.NS',
                    'BPCL.NS',
                    'BHARTIARTL.NS',
                    'BRITANNIA.NS',
                    'CIPLA.NS',
                    'COALINDIA.NS',
                    'DIVISLAB.NS',
                    'DRREDDY.NS',
                    'EICHERMOT.NS',
                    'GRASIM.NS',
                    'HCLTECH.NS',
                    'HDFCBANK.NS',
                    'HDFCLIFE.NS',
                    'HEROMOTOCO.NS',
                    'HINDALCO.NS',
                    'HINDUNILVR.NS',
                    'HDFC.NS',
                    'ICICIBANK.NS',
                    'ITC.NS',
                    'IOC.NS',
                    'INDUSINDBK.NS',
                    'INFY.NS',
                    'JSWSTEEL.NS',
                    'KOTAKBANK.NS',
                    'LT.NS',
                    'M&M.NS',
                    'MARUTI.NS',
                    'NTPC.NS',
                    'NESTLEIND.NS',
                    'ONGC.NS',
                    'POWERGRID.NS',
                    'RELIANCE.NS',
                    'SBILIFE.NS',
                    'SHREECEM.NS',
                    'SBIN.NS',
                    'SUNPHARMA.NS',
                    'TCS.NS',
                    'TATACONSUM.NS',
                    'TATAMOTORS.NS',
                    'TATASTEEL.NS',
                    'TECHM.NS',
                    'TITAN.NS',
                    'UPL.NS',
                    'ULTRACEMCO.NS',
                    'WIPRO.NS'
                ]
            if len(symbols) == 0:
                symbols = ['NIFTYBEES']
            sect_ret_results = []
            for symbol in symbols:
                data, xirr_value, inv_to_proceed, tot_inv, tot_ret = new_inv_test(symbol, 'EQ', start_date, end_date,
                                                                              no_of_shares, multiply, moving_average)
                sect_ret_results.append((symbol, xirr_value, inv_to_proceed, data[-1][0], data[-1][1]))
            return render(request, 'cal_returns/sect_return.html', {'form': form,
                                                                    'data': sect_ret_results,
                                                                    })
    else:
        form = SectReturnForm()
        return render(request, 'cal_returns/sect_return.html', {'form': form})

def get_json_inv_test(request):
    symbol = request.GET.get("symbol", None)
    if symbol:
        symbol = symbol
    else:
        symbol = 'NIFTYBEES.NS'
    #print(symbol)
    data, xirr_value, inv_to_proceed, tot_inv, tot_ret = new_inv_test(symbol, 'EQ', '2019-01-01', '2021-08-10',
                                                                      10, 1.4, 10)
    response = JsonResponse({'symbol':  symbol,
                             'xirr': xirr_value,
                             'inv_value': round(inv_to_proceed,2),
                             'data': data})
    return response
