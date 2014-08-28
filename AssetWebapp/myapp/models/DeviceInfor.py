'''
Created on Aug 15, 2014

@author: TuanNA
'''
from django.db import models
from myapp.models.DeviceProperties import DeviceProperties
from myapp.models.Device import Device

# Create your models here.
class DeviceInfor(models.Model):
    device = models.ForeignKey(Device)
    device_pro = models.ForeignKey(DeviceProperties)
    value = models.FloatField()
    status = models.CharField(max_length=1)
    class Meta:
        db_table = 'device_infor'
        app_label = 'myapp'
        permissions = (
            ("view_deviceinfor", "Can see list device infor"),
        )