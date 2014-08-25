'''
Created on Aug 15, 2014

@author: TuanNA
'''
from django.db import models

# Create your models here.
class Device(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    mac_add = models.CharField(max_length=30)
    connected_server = models.CharField(max_length=30)
    status = models.CharField(max_length=1)
    class Meta:
        db_table = 'device'