from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SharesForm
from .models import Shares, ShareList
from django.db.models import Avg, Count, Min, Sum
import yfinance as yf
import os
import sys
from django.http import JsonResponse
from django.templatetags.static import static
from .services.share_list import symbols
import json
#sys.path.append("../cal_returns/services")
#sys.path.append(os.path.abspath('cal_returns/services')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
#from ..cal_returns.services.xirr import xirr
from cal_returns.services.xirr import xirr

# Create your views here.

@login_required()
def load_shares(request):
    f = symbols.split('\n')
    for lines in f:
        #print(lines)
        is_exist = ShareList.objects.filter(text=f"{lines}.NS").exists()
        if not is_exist:
            obj = ShareList()
            obj.text = f"{lines}.NS"
            obj.name = f"{lines}.NS"
            obj.save()
    return JsonResponse({'result':'Data loaded successfully'})

@login_required()
def shares_details(request,pk):
    share_list = Shares.objects.filter(user=request.user).filter(symbol=pk).order_by('txn_date')
    units = {}
    investments = {}
    total_inv = 0
    total_div = 0
    for share in share_list:
        if share.symbol not in investments:
            investments[share.symbol] = []
            units[share.symbol] = 0
        multiply = 1
        #print(share)
        if share.txn_type == 'BUY':
            multiply = -1
            units[share.symbol] = units[share.symbol] + share.quantity
            total_inv = total_inv + share.quantity*share.share_price
        elif share.txn_type == 'SELL':
            units[share.symbol] = units[share.symbol] - share.quantity
        elif share.txn_type == 'DIV':
            total_div = total_div + share.share_price
        investments[share.symbol].append((share.txn_date,share.share_price*share.quantity*multiply))
    #print(investments)
    returns = {}
    for share in investments:
        symbol = yf.Ticker(share)
        hist = symbol.history(period='5d')
        returns[share] = {}
        investments[share].append((hist['Close'].index[-1].date(), hist['Close'].values[-1]*units[share]))
        returns[share]['units'] = units[share]
        #print(investments[share])
        returns[share]['returns'] = xirr(investments[share])*100
    return render(request, 'shares/share_list.html',
                  {'shares': share_list,
                   'symbol':pk,
                   'units': units[pk],
                   'total_inv':total_inv,
                   'xirr': xirr(investments[pk])*100,
                   'last_price': hist['Close'].values[-1],
                   'price_date': hist['Close'].index[-1],
                   'div':total_div,
                   'avg_price': total_inv/units[pk]
                   })


@login_required()
def shares_home(request):
    share_list = Shares.objects.filter(user=request.user).values('symbol','txn_type','txn_date','share_price','logo').annotate(quantity=Sum('quantity'))
    investments = {}
    units = {}
    returns = {}
    logos = {}
    for share in share_list:
        if share['symbol'] not in investments:
            investments[share['symbol']] = []
            units[share['symbol']] = 0
        multiply = 1
        if share['txn_type'] == 'BUY':
            multiply = -1
            units[share['symbol']] = units[share['symbol']] + share['quantity']
        elif share['txn_type'] == 'SELL':
            units[share['symbol']] = units[share['symbol']] - share['quantity']
        elif share['txn_type'] == 'DIV':
            pass
        investments[share['symbol']].append((share['txn_date'],share['share_price']*share['quantity']*multiply))
        logos[share['symbol']] = share['logo']
    for share in investments:
        symbol = yf.Ticker(share)
        hist = symbol.history(period='5d')

        returns[share] = {}
        investments[share].append((hist['Close'].index[-1].date(), hist['Close'].values[-1]*units[share]))
        returns[share]['units'] = units[share]
        #print(investments[share])
        returns[share]['returns'] = xirr(investments[share])*100
        returns[share]['logo'] = logos[share]

    return render(request, 'shares/shares_home.html',{'shares': share_list, 'returns': returns})

@login_required()
def add_shares(request):
    if request.method == 'POST':
        form = SharesForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            if ShareList.objects.filter(id=obj.symbol).exists():
                symbol_obj = get_object_or_404(ShareList,id=obj.symbol)
                symbol = yf.Ticker(symbol_obj.text)
                obj.symbol = symbol_obj.text
            elif ShareList.objects.filter(text=obj.symbol).exists():
                symbol = yf.Ticker(obj.symbol)
            logo = symbol.info['logo_url']
            obj.logo = logo

            obj.save()
        else:
            print(form)
        return redirect('shares')
    else:
        form = SharesForm()
        return render(request, 'shares/shares_form.html', {'form': form})

@login_required()
def update_share(request,pk):
    #print(pk)
    obj = get_object_or_404(Shares,id=pk)
    form = SharesForm(request.POST or None, instance = obj)
    if form.is_valid():
        form_obj = form.save(commit=False)
        symbol = yf.Ticker(obj.symbol)
        logo = symbol.info['logo_url']
        #print(logo)
        form_obj.logo = logo
        form_obj.save()
        return redirect('shares')

    # add form dictionary to context
    context ={}
    context["form"] = form
    return render(request, "shares/shares_form.html", context)

@login_required()
def get_share_list(request):
    query = request.GET.get('q')
    symbol_list = ShareList.objects.filter(text__contains=query).values()
    #print(symbol_list)
    return JsonResponse({'results':list(symbol_list)},safe=False)