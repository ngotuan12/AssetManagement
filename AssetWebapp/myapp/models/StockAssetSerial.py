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
from myapp.models.Supplier import Supplier
from myapp.models.Reason import Reason

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
    user_name = models.CharField(max_length=20,db_column="user_name")
    change_date = models.DateField(db_column="change_date")
    product_date = models.DateField(db_column="product_date")
    decision_date = models.DateField(db_column="decision_date")
    state = models.ForeignKey(List,db_column="state_id")
    goal = models.ForeignKey(List,db_column="goal_id")
    country = models.ForeignKey(Country,db_column="country_id")
    supplier = models.ForeignKey(Supplier,db_column="supplier_id")
    capital = models.ForeignKey(List,db_column="capital_id")
    amortize = models.ForeignKey(List,db_column="amortize_id")
    project_id = models.ForeignKey(List,db_column='project_id')
    reason = models.ForeignKey(Reason,db_column="reason_id")
    unit = models.CharField(max_length=100,db_column="unit")
    product_date = models.DateTimeField(db_column="product_date")
    power = models.IntegerField(db_column="power")
    interval = models.IntegerField(db_column="interval")
    source = models.CharField(max_length=100,db_column="source")
    decision_no = models.CharField(max_length=100,db_column="decision_no")
    document_status = models.CharField(max_length=5,db_column="document_status")
    num_sub = models.IntegerField(db_column="num_sub")
    parent_serial = models.CharField(max_length=5,db_column="parent_serial")
    name = models.CharField(max_length=50,db_column="name")
    note =  models.CharField(max_length=50,db_column="note")
    status = models.CharField(max_length=50,db_column="status")
    seri = models.CharField(max_length=50,db_column="seri")
    model = models.CharField(max_length=50,db_column="model")
    quantity = models.IntegerField(max_length=10,db_column="quantity")
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