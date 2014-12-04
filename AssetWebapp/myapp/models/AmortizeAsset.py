'''
Created on Aug 25, 2014

@author: TuanNA
'''

import datetime

from django.db import models

from myapp.models.List import List
from myapp.util.sequence import update_id


# Create your models here.
class AmortizeAsset(models.Model):
    id = models.IntegerField(primary_key=True,db_column="id")
    month = models.DateTimeField(db_column="month")
    serial_no = models.CharField(max_length=40,db_column="serial_no")    
    capital_id = models.FloatField(db_column="capital_id")
    amount = models.FloatField(db_column="amount")
    adjustment = models.FloatField(db_column="adjustment")
    amortize = models.ForeignKey(List,db_column='amortize_id')
    status = models.CharField(max_length=1,db_column="status")
    create_date = models.DateTimeField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),db_column="create_date")
    user_name = models.CharField(max_length=20,db_column="user_name")
    note = models.CharField(max_length=500,db_column="note")
    class Meta:
        db_table = 'asset_amortize'
        app_label = 'myapp'
        permissions = (
            ("view_list", "Can see list"),
        )
    @update_id
    def save(self):
        # Now actually save the object.
        super(AmortizeAsset, self).save()