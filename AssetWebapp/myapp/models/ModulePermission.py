# -*- coding: utf-8 -*-
'''
Created on Aug 15, 2014

@author: DienND
'''

from django.db import models


# Create your models here.
class ModulePermission(models.Model):
    name = models.CharField(max_length=200)
    permission_name = models.CharField(max_length=200)
    class Meta:
        db_table = 'module_permission'
        app_label = 'myapp'
        permissions = (
            ("increment_asset", "Có thể tăng tài sản"),
            ("decrement_asset", "Có thể giảm tài sản"),
        )