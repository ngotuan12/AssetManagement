'''
Created on Aug 25, 2014

@author: TuanNA
'''


from django.db import models

from myapp.models.Dept import Dept
from myapp.util.sequence import update_id
from myapp.models.Staff import Staff


# Create your models here.
class Stock(models.Model):
    id = models.IntegerField(primary_key=True,db_column="stock_id")
    dept = models.ForeignKey(Dept,db_column="dept_id")
    staff = models.ForeignKey(Staff,db_column="staff_id")
    code = models.CharField(max_length=40,db_column="code")
    name = models.CharField(max_length=200,db_column="name")
    note = models.CharField(max_length=500,db_column="note")
    class Meta:
        db_table = 'stock'
        app_label = 'myapp'
        permissions = (
            ("view_stock", "Can see list stock"),
        )
    @update_id
    def save(self):
        # Now actually save the object.
        super(Stock, self).save()