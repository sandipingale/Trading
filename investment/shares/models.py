from django.db import models

# Create your models here.


class Shares(models.Model):
    symbol = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    quantity = models.FloatField()
    share_price = models.FloatField()
    txn_date = models.DateField()


