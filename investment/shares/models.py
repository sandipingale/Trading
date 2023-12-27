from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Shares(models.Model):
    txn_types = [
        ('BUY', 'BUY'),
        ('SELL', 'SELL'),
        ('DIV','DIV')
    ]
    symbol = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    quantity = models.FloatField()
    share_price = models.FloatField()
    txn_date = models.DateField()
    txn_type = models.CharField(max_length=4, choices=txn_types)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    logo = models.CharField(max_length=150, null=True, blank=True)

class ShareList(models.Model):
    text = models.CharField(max_length=80)
    name = models.CharField(max_length=50)



