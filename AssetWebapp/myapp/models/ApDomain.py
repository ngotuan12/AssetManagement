'''
Created on Sep 10, 2014

@author: TuanNA
'''
'''
Created on Aug 15, 2014

@author: DienND
'''
from django.db import models

# Create your models here.
class ApDomain(models.Model):
    id = models.IntegerField(primary_key=True,db_column="id")
    code = models.CharField(max_length=40,db_column="code")
    name = models.CharField(max_length=200,db_column="name")
    type = models.CharField(max_length=40,db_column="type")
    value = models.CharField(max_length=40,db_column="value")
    description = models.CharField(max_length=500,db_column="description")
    class Meta:
        db_table = 'ap_domain'
        app_label = 'myapp'
        permissions = (
            ("view_ap_domain", "Can see list ap_domain"),
        )