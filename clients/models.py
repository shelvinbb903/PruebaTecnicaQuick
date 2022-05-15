from django.db import models

class Clients(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.CharField(max_length=12)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'clients'