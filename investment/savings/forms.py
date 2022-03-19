from django.forms import ModelForm
from .models import BankAccount, BankTransactions, TransactionCategory


class BankAccountForm(ModelForm):
    class Meta:
        model = BankAccount
        exclude = ['owner', 'balance']


class BankAccountTransactionForm(ModelForm):
    class Meta:
        model = BankTransactions
        exclude = ['owner', 'balance']


class TransactionCategoryForm(ModelForm):
    class Meta:
        model = TransactionCategory
        fields = ['category']
