from itertools import product
from tkinter import CASCADE
from django.db import models

from clients.models import Clients
from products.models import Products

class Bills(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=150)
    nit = models.CharField(max_length=30)
    code = models.CharField(max_length=150)
    
    class Meta:
        db_table = 'bills'
    
class BillsProducts(models.Model):
    id = models.AutoField(primary_key=True)
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'bills_products'