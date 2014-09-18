# -*- coding: utf-8 -*-
'''
Created on Aug 15, 2014

@author: DienND
'''
from django.db import models

from myapp.util.sequence import update_id
from AdminManagement.models.App import App


# Create your models here.
class Module(models.Model):
    id = models.IntegerField(primary_key=True,db_column="id")
    code = models.CharField(max_length=10,db_column="code")
    name = models.CharField(max_length=200,db_column="name")
    type = models.CharField(max_length=1,db_column="type")
    status = models.CharField(max_length=1,db_column="status")
    include_menu = models.CharField(max_length=10,db_column="include_menu")
    app = models.ForeignKey(App,db_column='app_id')
    parent = models.ForeignKey('self',db_column='parent_id',null=True)
    action = models.CharField(max_length=100,db_column="action")
    icon = models.CharField(max_length=200,db_column="icon")
    url = models.CharField(max_length=200,db_column="url")
    class Meta:
        db_table = 'module'
        app_label = 'AdminManagement'
    @update_id
    def save(self):
        # Now actually save the object.
        super(Module, self).save()