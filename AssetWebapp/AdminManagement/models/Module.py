# -*- coding: utf-8 -*-
'''
Created on Aug 15, 2014

@author: DienND
'''
import datetime

from django.contrib.contenttypes.models import ContentType
from django.db import models

from AdminManagement.models.App import App
from myapp.util.sequence import update_id
from django.contrib.auth.models import Permission


# Create your models here.
class Module(models.Model):
    id = models.IntegerField(primary_key=True,db_column="id")
    code = models.CharField(max_length=40,db_column="code")
    name = models.CharField(max_length=200,db_column="name")
    type = models.CharField(max_length=1,db_column="type")
    status = models.CharField(max_length=1,db_column="status")
    include_menu = models.CharField(max_length=10,db_column="include_menu")
    app = models.ForeignKey(App,db_column='app_id')
    content_type = models.ForeignKey(ContentType,db_column='content_type_id',null=True)
    permission = models.ForeignKey(Permission,db_column='permission_id',null=True)
    parent = models.ForeignKey('self',db_column='parent_id',null=True)
    action = models.CharField(max_length=200,db_column="action")
    icon_class = models.CharField(max_length=200,db_column="icon_class")
    url = models.CharField(max_length=300,db_column="url")
    create_date = models.DateTimeField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),db_column="create_date")
    user_name = models.CharField(max_length=20,db_column="user_name")
    ord = models.IntegerField(db_column="ord",default=1)
    class Meta:
        db_table = 'module'
        app_label = 'AdminManagement'
    @update_id
    def save(self):
        # Now actually save the object.
        super(Module, self).save()