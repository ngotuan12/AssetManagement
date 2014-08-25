'''
Created on Aug 15, 2014

@author: DienND
'''
from django.db import models

from myapp.models.Device import Device
from mongoengine.fields import ReferenceField
# Create your models here.
class DeviceLog(models.Model):
    device_id = ReferenceField(Device)
    reason_id = models.CharField(max_length=100)
    device_pro_id = ReferenceField('Area')
    issue_date = models.DateField()
    value = models.FloatField()
    status = models.CharField(max_length=1)
    class Meta:
        db_table = 'device_log'


