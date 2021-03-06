'''
Created on Aug 25, 2014

@author: TuanNA
'''

import datetime

from django.db import models

from myapp.util.sequence import update_id


# Create your models here.
class Asset(models.Model):
    id = models.IntegerField(primary_key=True,db_column="id")
    code = models.CharField(max_length=40,db_column="code")
    name = models.CharField(max_length=200,db_column="name")
    description = models.CharField(max_length=1,db_column="description")
    parent_id = models.ForeignKey('self',db_column='parent_id',null=True)
    list_level = models.CharField(max_length=1,db_column="list_level")
    status = models.CharField(max_length=1,db_column="status")
    interval = models.CharField(max_length=1,db_column="interval")
    class_group = models.CharField(max_length=10,db_column="class_group")
    create_datetime = models.DateTimeField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),db_column="create_datetime")
    user_name = models.CharField(max_length=20,db_column="user_name")
    parent_code = models.CharField(max_length=40,db_column="parent_code")
    account_no = models.CharField(max_length=40,db_column="account_no")
    class Meta:
        db_table = 'asset'
        app_label = 'myapp'
        permissions = (
            ("view_asset", "Can see list asset"),
        )
    @update_id
    def save(self):
        # Now actually save the object.
        super(Asset, self).save()