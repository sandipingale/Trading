from django.shortcuts import render

# Create your views here.

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import BankAccount, BankTransactions
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class BankAccountCreateView(LoginRequiredMixin,CreateView):
    model = BankAccount
    fields = ['acct_number', 'acct_name', 'acct_type', 'initial_balance']
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(BankAccountCreateView, self).form_valid(form)

class BankAccountUpdateView(LoginRequiredMixin,UpdateView):
    model = BankAccount
    fields = ['acct_number', 'acct_name', 'acct_type', 'initial_balance']


class BankTransactionsCreateView(LoginRequiredMixin,CreateView):
    model = BankTransactions
    fields = ['bank_account', 'txn_type', 'txn_category', 'txn_amount']
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(BankTransactionsCreateView, self).form_valid(form)

class BankTransactionsUpdateView(LoginRequiredMixin,UpdateView):
    model = BankTransactions
    fields = ['bank_account', 'txn_type', 'txn_category', 'txn_amount']



# Create your views here.
@login_required
def  get_saving_accounts(request):
    accounts = BankAccount.objects.filter(owner=request.user)
    print(request.user)
    context = {"accounts": BankAccount.objects.filter(owner=request.user)}
    for acct in accounts:
        print(acct.acct_number,acct.owner)
    return render(request, 'savings/account_list.html', context=context)