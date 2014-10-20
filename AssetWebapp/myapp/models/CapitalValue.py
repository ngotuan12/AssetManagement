'''
Created on Aug 25, 2014

@author: TuanNA
'''

import datetime

from django.db import models

from myapp.util.sequence import update_id
from myapp.models.StockAssetSerial import StockAssetSerial
from myapp.models.List import List

# Create your models here.
class CapitalValue(models.Model):
    id = models.IntegerField(primary_key=True,db_column="id")
    stock_asset_serial = models.ForeignKey(StockAssetSerial,db_column='stock_asset_serial_id')
    capital = models.ForeignKey(List,db_column="capital_id")
    original_value = models.FloatField(db_column="original_value")
    remain_value = models.FloatField(db_column="remain_value")
    description =  models.CharField(max_length=100,db_column="description")
    class Meta:
        db_table = 'capital_value'
        app_label = 'myapp'
        permissions = (
            ("view_capital_value", "Can see list capital value"),
        )
    @update_id
    def save(self):
        # Now actually save the object.
        super(CapitalValue, self).save()