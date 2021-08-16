from django.shortcuts import render
from django.http import JsonResponse
import yfinance as yf
import json
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.

def charts(request):
    return render(request,'chartapp/chartbase.html',{})

def analysis(request):
    symbol = request.GET.get("symbol", None)
    if symbol:
        symbol = symbol
    else:
        symbol = 'NIFTYBEES.NS'


    start_date = '2021-01-01'
    end_date = '2021-08-16'
    moving_average = 10
    no_of_shares = 10
    symbol = yf.Ticker(symbol)
    hist = symbol.history(start=start_date, end=end_date)
    df = hist
    df = df.reset_index()
    df['MA'] = df['Close'].rolling(window=moving_average).mean()
    df['avg_diff'] = (df['Close'] - df['MA']) / df['MA'] * 100
    df['inv_value'] = df['Close'] * -1 * no_of_shares
    df['just_date'] = df['Date'].dt.date
    print(df['just_date'].tolist())

    response = {
        'type': 'line',
        'data':{
            'labels': df['just_date'].tolist(),
            'datasets': [
                {
                    'label': 'Average Difference',
                    'data': df['avg_diff'].tolist(),
                    'borderColor': 'rgb(75, 192, 192)',
                    'fill': False,
                    'tension': 0.5
                }
            ],
        },
        'options':{
            'responsive': True,
            'elements':{
                'point':{
                    'pointRadius':0.5
                }
            }
        }
    }

    response1 = {
        'type': 'line',
        'data':{
            'labels': df['just_date'].tolist(),
            'datasets': [
                {
                    'label': 'Close Price',
                    'data': df['Close'].tolist(),
                    'borderColor': 'rgb(75, 192, 192)',
                    'fill': False,
                    'tension': 0.1
                }
            ],
        },
        'options':{
            'responsive': True,
            'elements':{
                'point':{
                    'pointRadius':0.1
                }
            }
        }
    }
    #return response

    return render(request,'chartapp/analysis.html',{'xxxx':json.dumps(response,cls=DjangoJSONEncoder),'yyyy':json.dumps(response1,cls=DjangoJSONEncoder)})

def get_chart_data(request):
    chart_type = request.GET.get("type", None)
    if chart_type:
        chart_type = chart_type
    else:
        chart_type = 'bar'
    print(chart_type)
    labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
    response = JsonResponse({
                            'type': chart_type,
                            'data':{
                                'labels': labels,
                                'datasets': [
                                    {
                                        'label': '# of Votes',
                                        'data': [20, 19, 3, 5, 2, 3],
                                        'backgroundColor': [
                                            'rgba(255, 99, 132,1.8)',
                                            'rgba(54, 162, 235, 1.5)',
                                            'rgba(255, 206, 86, 1.2)',
                                            'rgba(75, 192, 192, 0.8)',
                                            'rgba(153, 102, 255, 0.8)',
                                            'rgba(255, 159, 64, 0.8)'
                                        ],
                                        'borderColor': [
                                            'rgba(255, 99, 132, 1)',
                                            'rgba(54, 162, 235, 1)',
                                            'rgba(255, 206, 86, 1)',
                                            'rgba(75, 192, 192, 1)',
                                            'rgba(153, 102, 255, 1)',
                                            'rgba(255, 159, 64, 1)'
                                        ],
                                        'borderWidth': 1
                                    }
                                ],
                            },
                            'options':{
                                'scales':{
                                    'y':{
                                        'beginAtZero': True
                                    }
                                },
                                'responsive': True,

                            }
                            },
                            )
    return response
