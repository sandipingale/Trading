from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class BankAccount(models.Model):
    acct_types = [
        ('SAVING', 'SAVING'),
        ('FD', 'FD'),
        ('PPF', 'PPF')
    ]

    acct_number = models.CharField(max_length=30)
    acct_type = models.CharField(max_length=10, choices=acct_types)
    acct_name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    initial_balance = models.FloatField()
    balance = models.FloatField(default=0)

    def get_absolute_url(self):
        return reverse('bank-acct-details')


class TransactionCategory(models.Model):
    category = models.CharField(max_length=50)


class BankTransactions(models.Model):
    txn_type_choices = [
        ('CREDIT', 'CREDIT'),
        ('DEBIT', 'DEBIT')
        ]

    txn_type = models.CharField(max_length=10, choices=txn_type_choices)
    txn_amount = models.FloatField()
    bank_account = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    txn_category = models.ForeignKey(TransactionCategory, on_delete=models.SET_NULL, null=True, blank=True)

