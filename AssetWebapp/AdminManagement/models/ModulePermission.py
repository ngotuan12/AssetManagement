# -*- coding: utf-8 -*-
'''
Created on Aug 15, 2014

@author: DienND
'''
from django.db import models

from AdminManagement.models.Module import Module
from django.contrib.auth.models import Permission


# Create your models here.
class ModulePermission(models.Model):
    id = models.IntegerField(primary_key=True,db_column="id")
    module = models.ForeignKey(Module,db_column='module_id')
    permission = models.ForeignKey(Permission,db_column='permission_id')
    class Meta:
        db_table = 'module_permission'
