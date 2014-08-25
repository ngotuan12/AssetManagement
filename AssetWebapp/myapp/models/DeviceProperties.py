'''
Created on Aug 15, 2014

@author: TuanNA
'''
from django.db import models

# Create your models here.
class DeviceProperties(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    type = models.CharField(max_length=1)
    min = models.FloatField()
    max = models.FloatField()
    min_alarm = models.FloatField()
    max_alarm = models.FloatField()
    symbol = models.CharField(max_length=15)
    class Meta:
        db_table = 'device_properties'
