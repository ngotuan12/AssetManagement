# -*- coding: utf-8 -*-
'''
Created on Aug 15, 2014

@author: DienND
'''
from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import ugettext as _

from AdminManagement.models.Module import Module


# Create your models here.
class ModulePermission(models.Model):
    id = models.IntegerField(primary_key=True,db_column="id")
    module = models.ForeignKey(Module,db_column='module_id')
    permission = models.ForeignKey(Permission,db_column='permission_id')
    class Meta:
        db_table = 'module_permission'
        app_label = 'myapp'
        permissions = (
            ("increment_asset", _(u"Có thể tăng tài sản")),
            ("decrement_asset", _(u"Có thể giảm tài sản")),
            ("evaluation_asset", _(u"Có thể đánh giá lại tài sản")),
            ("transfer_asset", _(u"Có thể chuyển đổi tài sản")),
            ("verify_asset", _(u"Có thể kiểm kê tài sản")),
            ("verify_asset_edit", _(u"Có thể sửa kiểm kê tài sản")),
            ("view_asset", _(u"Có thể tra cứu tài sản")),
            ("release_asset", _(u"Có thể tách tài sản")),
            ("join_asset", _(u"Có thể gộp tài sản")),
            ("amortize_asset", _(u"Có thể tính khấu hao tài sản")),
            ("inventory_asset_report", _(u"Có thể xuất báo cáo kiểm kê tài sản")),
            ("summarize_inventorry_asset_report", _(u"Có thể xuất báo cáo tổng hợp kiểm kê tài sản")),
            ("upgrade_asset", _(u"Có thể nâng cấp tài sản")),
            ("asset_type", _(u"Có thể quản lý loại tài sản")),
            ("edit_increment_asset", _(u"Có thể sửa thông tin tài sản")),
            ("view_department", _(u"Xem thông tin phòng ban")),
            ("add_department", _(u"Có thể sửa thông tin tài sản")),
            ("edit_department", _(u"Có thể sửa thông tin tài sản")),
            ("delete_department", _(u"Có thể sửa thông tin tài sản")),
            ("view_asset_type", _(u"Có thể xem danh sách loại tài sản")),
            ("add_asset_type", _(u"Có thể thêm loại tài sản")),
            ("edit_asset_type", _(u"Có thể sửa loại tài sản")),
            ("delete_asset_type", _(u"Có thể xóa loại tài sản")),
            ("view_reason", _(u"Có thể xem danh sách lý do")),
            ("add_reason", _(u"Có thể thêm lý do")),
            ("change_reason", _(u"Có thể sửa lý do")),
            ("delete_reason", _(u"Có thể xóa lý do")),
            ("delete_reason", _(u"Có thể xóa lý do")),
            ("asset_project_report", _(u"Có thể tạo báo cáo tài sản theo dự án"))
        )