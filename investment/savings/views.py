from django.shortcuts import render, redirect, get_object_or_404
from .models import BankAccount, BankTransactions, TransactionCategory
from .forms import BankAccountForm, BankAccountTransactionForm, TransactionCategoryForm
from django.contrib.auth.decorators import login_required


@login_required
def get_saving_accounts(request):
    accounts = BankAccount.objects.filter(owner=request.user)
    print(request.user)
    context = {"accounts": BankAccount.objects.filter(owner=request.user)}
    for acct in accounts:
        print(acct.acct_number, acct.owner)
    return render(request, 'savings/account_list.html', context=context)


@login_required()
def create_account_view(request):
    form = BankAccountForm()
    if request.method == 'GET':
        return render(request, "savings/bankaccount_form.html", {'form': form})
    elif request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
        else:
            print(form)
        return redirect('bank-acct-details')


@login_required()
def update_bank_account(request, pk):
    obj = get_object_or_404(BankAccount, id=pk)
    form = BankAccountForm(request.POST or None, instance=obj)
    error = ""
    if request.user != obj.owner:
        error = "You are not allowed to update this account"
    if form.is_valid() and request.user == obj.owner:
        form_obj = form.save(commit=False)
        form_obj.save()
        return redirect('bank-acct-details')
    if request.user != obj.owner:
        form = BankAccountForm()
    # add form dictionary to context
    context = {"form": form, "error": error}
    return render(request, "savings/bankaccount_form.html", context)


@login_required()
def get_bank_transaction(request):
    transactions = BankTransactions.objects.filter(owner=request.user)
    print(transactions)
    context = {"transactions": transactions}
    return render(request, "savings/transaction_list.html", context=context)

@login_required()
def get_bank_transaction_for_account(request,pk):
    transactions = BankTransactions.objects.filter(owner=request.user).filter(bank_account=pk)
    print(transactions)
    context = {"transactions": transactions}
    return render(request, "savings/transaction_list.html", context=context)

@login_required()
def create_bank_transaction(request):
    form = BankAccountTransactionForm()

    if request.method == 'GET':
        accounts = BankAccount.objects.filter(owner=request.user)
        txn_categories = TransactionCategory.objects.all()
        return render(request, "savings/banktransactions_form.html",
                      {'form': form, 'accounts': accounts, 'categories': txn_categories})
    elif request.method == 'POST':
        form = BankAccountTransactionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            print(obj.bank_account)
            obj.save()
        else:
            print(form)
        print("I am in new method")
        return redirect('get_acct_transaction')


@login_required()
def update_bank_transaction(request, pk):
    obj = get_object_or_404(BankTransactions, id=pk)
    form = BankAccountTransactionForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('get_acct_transaction')
    accounts = BankAccount.objects.filter(owner=request.user)
    txn_categories = TransactionCategory.objects.all()
    context = {"form": form, 'accounts': accounts, 'categories': txn_categories}
    return render(request, "savings/banktransactions_form.html", context)


@login_required
def get_accounts_categories(request):
    categories = TransactionCategory.objects.all()
    context = {"categories": categories}
    return render(request, 'savings/category_list.html', context=context)


@login_required()
def create_account_category(request):
    form = TransactionCategoryForm()

    if request.method == 'GET':
        return render(request, "savings/categories_form.html", {'form': form})
    elif request.method == 'POST':
        form = TransactionCategoryForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form)
        return redirect('bank-acct-categories')


@login_required()
def update_account_category(request, pk):
    obj = get_object_or_404(TransactionCategory, id=pk)
    print(obj)
    form = TransactionCategoryForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('bank-acct-categories')
    context = {"form": form}
    return render(request, "savings/categories_form.html", context)
