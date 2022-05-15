from django.db import models

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=150)
    password = models.CharField(max_length=200)
    active = models.BooleanField()
    
    class Meta:
        db_table = 'users'
        
class User:
    pass