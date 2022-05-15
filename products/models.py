from django.db import models

class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=18, decimal_places=2)
    
    class Meta:
        db_table = 'products'