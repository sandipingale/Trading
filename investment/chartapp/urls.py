from django.urls import path
from . import views

urlpatterns = [
    path('charts', views.charts, name='charts'),
    path('chartdata',views.get_chart_data,name='chart-data'),
    path('analysis',views.analysis,name='analysis')

]