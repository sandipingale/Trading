from django.shortcuts import render, get_object_or_404, HttpResponse
import sys
from datetime import date, datetime
from .forms import StockForm, InvStockForm, SectReturnForm
from .services.query_stocks import  new_inv_test,get_results
from django.http import JsonResponse
import os
from django.contrib.auth.decorators import login_required
sys.path.append(os.path.abspath('.'))
from shares.models import ShareList
from django.contrib.auth.decorators import login_required
from registrations.decorators import allowed_user
from render_block import render_block_to_string
import json


@login_required()
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

@login_required()
@allowed_user(['test_group'])
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
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            no_of_shares = 1 
            multiply = 1.4 
            moving_average = 10 
            moving_average = int(form.cleaned_data['risk_ape'])

            data, xirr_value, inv_to_proceed, tot_inv, tot_ret = new_inv_test(symbol, 'EQ', start_date, end_date,
                                                                          no_of_shares, multiply, moving_average)
            abs_ret = (tot_ret - tot_inv)/tot_inv * 100
            date_list = [datetime(year=x[0].year, month=x[0].month, day=x[0].day).timestamp()*1000+86400000 for x in data]
            price_list = [round(x[1],2) for x in data]
            price_list[-1] = price_list[-2]
            price1_list = [round(x[2],2) for x in data]
            msg = f"{price_list[-1]} invested would have given {price1_list[-1]}"
            html = render_block_to_string('cal_returns/inv_return_test_par.html', 'inv-test-result',{'form': form,
                                                                                     'data': data,
                                                                                     'symbol': symbol,
                                                                                     'xirr': xirr_value,
                                                                                     'inv_to_proceed': inv_to_proceed,
                                                                                     'total_inv': tot_inv,
                                                                                     'total_ret': tot_ret,
                                                                                     'abs_return': abs_ret,
                                                                                     'date_list': date_list,
                                                                                     'price_list': price_list,
                                                                                     'price1_list': price1_list,
                                                                                     'msg':msg})
            return HttpResponse(html)

    else:
        form = InvStockForm()
        return render(request, 'cal_returns/inv_return_test_par.html', {'form': form})


@login_required()
@allowed_user(['shares_group'])
def sect_return(request):
    if request.method == 'POST':
        form = SectReturnForm(request.POST)
        if form.is_valid():
            sector = form.cleaned_data['sector']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            no_of_shares = 10 
            multiply = 1.4 
            moving_average = 10 
            symbols = []
            if sector == 'IT':
                symbols = ['WIPRO.NS', 'TCS.NS', 'INFY.NS', 'TECHM.NS', 'NIITLTD.NS', 'HCLTECH.NS', 'TATAELXSI.NS', 'MINDTREE.NS', ]
            if sector == 'Auto':
                symbols = ['ASHOKLEY.NS', 'HEROMOTOCO.NS', 'M&M.NS', 'APOLLOTYRE.NS', 'MRF.NS', 'BAJAJ-AUTO.NS', 'MARUTI.NS', 'EICHERMOT.NS',
                           'TVSMOTOR.NS', 'TATAMOTORS.NS', 'BOSCHLTD.NS', 'EXIDEIND.NS', 'AMARAJABAT.NS', 'BHARATFORG.NS']
            if sector == 'Bank':
                symbols = ['IDFCFIRSTB.NS', 'INDUSINDBK.NS', 'YESBANK.NS', 'SBIN.NS', 'AXISBANK.NS', 'PNB.NS', 'HDFCBANK.NS', 'BANKBARODA.NS',
                           'RBLBANK.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS', 'FEDERALBNK.NS']
            if sector == 'ETF':
                symbols = ['NIFTYBEES.NS', 'KOTAKBKETF.NS', 'CPSEETF.NS', 'SETFNIFBK.NS', 'SETFNIF50.NS', 'BANKBEES.NS', 'ICICINIFTY.NS',
                           'GOLDBEES.NS', 'ICICILIQ.NS']
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
            html =  render_block_to_string('cal_returns/sect_return.html', 'sec_return_result', {'form': form,
                                                                    'data': sect_ret_results,
                                                                    })
            return HttpResponse(html)
    else:
        form = SectReturnForm()
        return render(request, 'cal_returns/sect_return.html', {'form': form})

@login_required()
@allowed_user(['shares_group'])
def get_json_inv_test(request):
    post_msg = json.loads(request.body.decode("utf-8"))
    symbol = post_msg.get("symbol")
    start_date = post_msg.get("start_date")
    end_date = post_msg.get("end_date")
    category = post_msg.get("category")
    if symbol:
        symbol = symbol
    else:
        symbol = 'NIFTYBEES.NS'
    symbolobj = ShareList.objects.filter(text=symbol)
    symbol = symbolobj[0].name

    data, xirr_value, inv_to_proceed, tot_inv, tot_ret = new_inv_test(symbol, 'EQ', start_date, end_date,
                                                                      10, 1.4, int(category))
    abs_ret = (tot_ret - tot_inv)/tot_inv * 100
    date_list = [datetime(year=x[0].year, month=x[0].month, day=x[0].day).timestamp()*1000+86400000 for x in data]
    price_list = [round(x[1],2) for x in data]
    price_list[-1] = price_list[-2]
    price1_list = [round(x[2],2) for x in data]
    msg = f"{price_list[-1]} invested would have given {price1_list[-1]}"
    response = JsonResponse({'symbol':  symbol,
                             'xirr': xirr_value,
                             'inv_value': round(inv_to_proceed,2),
                             'inv_to_proceed': round(inv_to_proceed,2),
                            'total_inv': round(tot_inv,2),
                            'total_ret': round(tot_ret,2),
                            'abs_return': round(abs_ret,2),
                            'date_list': date_list,
                            'price_list': price_list,
                            'price1_list': price1_list,
                            'msg':msg,
                             'data': data})
    return response

