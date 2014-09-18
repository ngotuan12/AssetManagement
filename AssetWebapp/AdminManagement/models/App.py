# -*- coding: utf-8 -*-
'''
Created on Aug 15, 2014

@author: DienND
'''
from django.db import models

from myapp.util.sequence import update_id


# Create your models here.
class App(models.Model):
    id = models.IntegerField(primary_key=True,db_column="id")
    code = models.CharField(max_length=10,db_column="code")
    name = models.CharField(max_length=200,db_column="name")
    type = models.CharField(max_length=10,db_column="type")
    class Meta:
        db_table = 'app'
        app_label = 'AdminManagement'
    @update_id
    def save(self):
        # Now actually save the object.
        super(App, self).save()