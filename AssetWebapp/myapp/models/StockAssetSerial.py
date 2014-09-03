'''
Created on Aug 25, 2014

@author: TuanNA
'''

import datetime

from django.db import models

from myapp.util.sequence import update_id
from myapp.models.Stock import Stock
from myapp.models.Asset import Asset


# Create your models here.
class StockAssetSerial(models.Model):
    id = models.IntegerField(primary_key=True,db_column="id")
    stock = models.ForeignKey(Stock,db_column='stock_id')
    asset = models.ForeignKey(Asset,db_column="asset_id")
    serial = models.CharField(max_length=100,db_column="serial")
    original_value = models.FloatField(db_column="original_value")
    remain_value = models.FloatField(db_column="remain_value")
    import_date = models.DateField(db_column="import_date")
    status = models.CharField(max_length=1,db_column="status")
    interval = models.CharField(max_length=1,db_column="interval")
    class_group = models.CharField(max_length=10,db_column="class_group")
    create_datetime = models.DateTimeField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),db_column="create_datetime")
    user_name = models.CharField(max_length=20,db_column="user_name")
    parent_code = models.CharField(max_length=40,db_column="parent_code")
    class Meta:
        db_table = 'stock_asset_serial'
        app_label = 'myapp'
        permissions = (
            ("view_stock_asset_serial", "Can see list stock asset serial"),
        )
    @update_id
    def save(self):
        # Now actually save the object.
        super(StockAssetSerial, self).save()