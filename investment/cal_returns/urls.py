from django.urls import path
from . import views

urlpatterns = [
    path('stock_details', views.stock_details, name='stock_details'),
    path('inv_return_test', views.inv_return_test, name='inv_return_test'),
    path('sect_return', views.sect_return, name='sect_return'),
    path('home', views.home, name='home'),
]