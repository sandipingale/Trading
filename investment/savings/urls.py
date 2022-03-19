from django.urls import path
from . import views
urlpatterns = [
    path('savings', views.get_saving_accounts,name='bank-acct-details'),
    path('savings/add', views.BankAccountCreateView.as_view(),name='add_savings_acct'),
    path('savings/update/<int:pk>', views.BankAccountUpdateView.as_view(),name='update_savings_acct'),
    path('transaction/add', views.BankTransactionsCreateView.as_view(),name='add_acct_transaction'),
    path('transaction/update/<int:pk>', views.BankTransactionsUpdateView.as_view(),name='update_acct_transaction'),
]
