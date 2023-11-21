from django.db import models

# Create your models here.


class CurrencyRate(models.Model):
    date = models.DateField()
    cur_code = models.CharField(max_length=3)
    cur_official_rate = models.DecimalField(max_digits=10, decimal_places=4)
