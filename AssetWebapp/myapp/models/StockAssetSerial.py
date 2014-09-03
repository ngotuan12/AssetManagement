'''
Created on Aug 25, 2014

@author: TuanNA
'''

from django.db import models

from myapp.models.Asset import Asset
from myapp.models.Country import Country
from myapp.models.List import List
from myapp.models.Stock import Stock
from myapp.util.sequence import update_id


# Create your models here.
class StockAssetSerial(models.Model):
    id = models.IntegerField(primary_key=True,db_column="id")
    stock = models.ForeignKey(Stock,db_column='stock_id')
    asset = models.ForeignKey(Asset,db_column="asset_id")
    serial = models.CharField(max_length=100,db_column="serial")
    original_value = models.FloatField(db_column="original_value")
    remain_value = models.FloatField(db_column="remain_value")
    import_date = models.DateField(db_column="import_date")
    use_date = models.DateField(db_column="use_date")
    change_date = models.DateField(db_column="change_date")
    state = models.ForeignKey(List,db_column="state_id")
    goal = models.ForeignKey(List,db_column="goal_id")
    country = models.ForeignKey(Country,db_column="country_id")
    capital = models.ForeignKey(List,db_column="capital_id")
    amortize = models.ForeignKey(List,db_column="amortize_id")
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