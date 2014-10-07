'''
Created on Aug 25, 2014

@author: TuanNA
'''

from django.db import models

from myapp.models.List import List
from myapp.models.StockAssetSerial import StockAssetSerial
from myapp.util.sequence import update_id
from myapp.models.Stock import Stock
# Create your models here.
class StockAssetSerialHis(models.Model):
    id = models.IntegerField(primary_key=True,db_column="id")
    stock_asset_serial = models.ForeignKey(StockAssetSerial,db_column='stock_asset_serial_id')
    serial = models.CharField(max_length=100,db_column="serial")
    action_type = models.CharField(max_length=10,db_column='action_type')
    original_value = models.FloatField(db_column="original_value")
    remain_value = models.FloatField(db_column="remain_value")
    state = models.ForeignKey(List,db_column="state_id")
    goal = models.ForeignKey(List,db_column="goal_id")
    capital = models.ForeignKey(List,db_column="capital_id")
    amortize = models.ForeignKey(List,db_column="amortize_id")
    interval = models.IntegerField(db_column="interval")
    note =  models.CharField(max_length=50,db_column="note")
    change_date = models.DateField(db_column="change_date")
    user_name = models.CharField(max_length=20,db_column="user_name")
    stock = models.ForeignKey(Stock,db_column="stock_id")
    
    class Meta:
        db_table = 'stock_asset_serial_his'
        app_label = 'myapp'
        permissions = (
            ("view_stock_asset_serial_his", "Can see list stock asset serial his"),
        )
    @update_id
    def save(self):
        # Now actually save the object.
        super(StockAssetSerialHis, self).save()