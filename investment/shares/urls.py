from . import views
from django.urls import path
urlpatterns = [
    path('shares', views.shares_home, name='shares'),
    path('share_details/<pk>/', views.shares_details, name='share_details'),
    path('add_shares', views.add_shares, name='add_shares'),
    path('update_share/<int:pk>', views.update_share, name='update_share'),
    path('get_share_list', views.get_share_list, name='get_share_list'),
    path('load_shares', views.load_shares, name='load_shares')
]
