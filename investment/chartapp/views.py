from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def charts(request):
    return render(request,'chartapp/chartbase.html',{})

def get_chart_data(request):
    labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
    response = JsonResponse({
                            'type': 'doughnut',
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
                                'responsive': True
                            }
                            },
                            )
    return response
