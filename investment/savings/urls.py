from django.urls import path
from . import views
urlpatterns = [
    path('savings', views.get_saving_accounts, name='bank-acct-details'),
    path('savings/add', views.create_account_view, name='add_savings_acct'),
    path('savings/update/<int:pk>', views.update_bank_account, name='update_savings_acct'),

    path('transaction', views.get_bank_transaction, name='get_acct_transaction'),
    path('transaction/add', views.create_bank_transaction, name='add_acct_transaction'),
    path('transaction/update/<int:pk>', views.update_bank_transaction, name='update_acct_transaction'),

    path('categories', views.get_accounts_categories, name='bank-acct-categories'),
    path('categories/add', views.create_account_category, name='add_savings_acct_category'),
    path('categories/update/<int:pk>', views.update_account_category, name='update_savings_acct_category'),
]
