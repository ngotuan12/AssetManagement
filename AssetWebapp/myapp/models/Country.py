'''
Created on Aug 25, 2014

@author: TuanNA
'''

import datetime

from django.db import models

from myapp.util.sequence import update_id


# Create your models here.
class Country(models.Model):
    id = models.IntegerField(primary_key=True,db_column="id")
    code = models.CharField(max_length=40,db_column="country_code")
    name = models.CharField(max_length=200,db_column="country_name")
    po_code = models.CharField(max_length=40,db_column="po_code") 
    create_datetime = models.DateTimeField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),db_column="create_datetime")
    user_name = models.CharField(max_length=20,db_column="user_name")
    class Meta:
        db_table = 'country'
        app_label = 'myapp'
        permissions = (
            ("view_country", "Can see list country"),
        )
    @update_id
    def save(self):
        # Now actually save the object.
        super(Country, self).save()