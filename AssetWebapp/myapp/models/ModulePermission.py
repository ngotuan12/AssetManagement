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
            ("evaluation_asset", "Có thể đánh giá lại tài sản"),
            ("transfer_asset", "Có thể chuyển đổi tài sản"),
            ("verify_asset", "Có thể kiểm kê tài sản"),
            ("verify_asset_edit", "Có thể sửa kiểm kê tài sản"),
            ("view_asset", "Có thể tra cứu tài sản"),
            ("release_asset", "Có thể tách tài sản"),
            ("join_asset", "Có thể gộp tài sản"),
            ("amortize_asset", "Có thể tính khấu hao tài sản"),
            ("inventory_asset_report", "Có thể xuất báo cáo kiểm kê tài sản"),
            ("summarize_inventorry_asset_report", "Có thể xuất báo cáo tổng hợp kiểm kê tài sản")
        )