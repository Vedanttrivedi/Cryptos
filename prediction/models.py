from django.db import models
from django.db.models.base import Model
from datetime import datetime

# Create your models here.

class Currency(models.Model):
    currency_name = models.CharField(max_length=50)
    currency_highprice = models.DecimalField(max_digits=20,decimal_places=2)
    currency_lowprice = models.DecimalField(max_digits=20,decimal_places=2)
    currency_predictionPrice = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    currency_icon = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.currency_name}"