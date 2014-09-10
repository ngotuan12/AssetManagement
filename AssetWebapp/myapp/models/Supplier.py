'''
Created on Aug 25, 2014

@author: TuanNA
'''

import datetime

from django.db import models

from myapp.util.sequence import update_id


# Create your models here.
class Supplier(models.Model):
    id = models.IntegerField(primary_key=True,db_column="id")
    code = models.CharField(max_length=10,db_column="supplier_code")
    name = models.CharField(max_length=200,db_column="supplier_name")
    status = models.CharField(max_length=1,db_column="supplier_status")
    parent_id = models.ForeignKey('self',db_column='parent_id',null=True)
    address = models.CharField(max_length=300,db_column="address")
    tel = models.CharField(max_length=100,db_column="tel")
    fax = models.CharField(max_length=100,db_column="fax")
    contact_person = models.CharField(max_length=200,db_column="contact_person")
    create_datetime = models.DateTimeField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),db_column="create_datetime")
    user_name = models.CharField(max_length=20,db_column="user_name")
    parent_code = models.CharField(max_length=40,db_column="parent_code")
    class Meta:
        db_table = 'supplier'
        app_label = 'myapp'
        permissions = (
            ("view_supplier", "Can see list supplier"),
        )
    @update_id
    def save(self):
        # Now actually save the object.
        super(Supplier, self).save()