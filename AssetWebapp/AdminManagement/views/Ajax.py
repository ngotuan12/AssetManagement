# -*- coding: utf-8 -*-
'''
Created on Sep 18, 2014

@author: TuanNA
'''
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_http_methods

from AdminManagement.models.App import App
from AdminManagement.models.Module import Module
from myapp.util.DateEncoder import DateEncoder


@require_http_methods(["POST",])
def ajax_app_infor(request):
    try:
        app_id = request.POST['app_id']
        apps = App.objects.filter(id=app_id)
        infors =[]
        for app in apps:
            infors.append(model_to_dict(app))
        return HttpResponse(json.dumps({'apps':infors},cls=DateEncoder) ,content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({"error": str(ex)}),content_type="application/json")
@require_http_methods(["POST",])
@login_required(login_url='/login/')
def ajax_save_user_permission(request,user_id):
    try:
        user = User.objects.get(id=user_id)
        permissions = json.loads(request.POST['permissions'])
        print permissions
        #clear permissions
        user.user_permissions.clear()
        #update permissions
        permissions_qs = Permission.objects.filter(id__in = permissions)
        for permission in permissions_qs:
            user.user_permissions.add(permission)
        return HttpResponse(json.dumps({"handle":"success",}) ,content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({"handle":"error","message": str(ex)}),content_type="application/json")
@require_http_methods(["POST",])
@login_required(login_url='/login/')
def ajax_user_permission(request,user_id):
    try:
        user = User.objects.get(id=user_id)
        permissions = user.user_permissions.values_list('id', flat=True)
        module_qs = Module.objects.raw("""
                                SELECT id,name,code,status,parent_id,
                                connect_by_isleaf is_leaf 
                                FROM module
                                START WITH parent_id IS NULL 
                                CONNECT BY PRIOR id = parent_id 
                                ORDER SIBLINGS BY app_id,ord 
                                """)
        modules = []
#         print serializers.serialize('json', module_qs, fields=('id','code','name'))
        for module in module_qs:
            row = {}
            row.update({'id':module.id})
            row.update({'app_id':module.app.id})
            row.update({'code':module.code})
            row.update({'name':module.name})
            row.update({'status':module.status})
            row.update({'action':module.action})
            row.update({'icon_class':module.icon_class})
            row.update({'url':module.url})
            row.update({'create_date':module.create_date.strftime('%Y-%m-%d %H:%M:%S')})
            row.update({'user_name':module.user_name})
            row.update({'ord':module.ord})
#             type
            module_type = _(u"unknown")
            icon = None
            if module.type == "R":
                module_type = _(u"Hệ thống")
                icon = '/images/module/home.png'
            elif module.type == "G":
                module_type = _(u"Nhóm chức năng")
                icon = '/images/module/group.png'
            elif module.type == "M":
                module_type = _(u"Chức năng")
                icon = '/images/module/module.png'
            elif module.type == "P":
                module_type = _(u"Quyền hạn")
                row.update({'permission_id':module.permission.id})
                try:
                    permissions.get(id=module.permission.id)
                    row.update({'checked':True})
                except ObjectDoesNotExist:
                    row.update({'checked':False})
                icon = '/images/module/permission.png'
            row.update({'module_type':module_type})
            row.update({'type':module.type})
            row.update({'icon':icon})
#             parent
            if module.parent is not None:
                row.update({'parent_id':module.parent.id})
                row.update({'parent_name':module.parent.name})
            else:
                row.update({'open':True,'iconOpen':'/images/module/home.png', 'iconClose':'/images/module/home.png'})
            modules.append(row)
        return HttpResponse(
                            json.dumps({
                                        "handle":"success",
                                        "user": model_to_dict(user),
                                        'modules':modules,
                                        'apps':serializers.serialize('python', App.objects.filter(status='1'), fields=('id','code','name')),
                                        },cls=DateEncoder) 
                            ,content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({"handle":"error","message": str(ex)}),content_type="application/json")
@require_http_methods(["POST",])
@login_required(login_url='/login/')
def ajax_app_module(request):
    try:
        app_id = request.POST['app_id']
        module_qs = Module.objects.raw("""
                                SELECT id,name,code,status,parent_id,
                                connect_by_isleaf is_leaf 
                                FROM module
                                WHERE app_id= %s
                                START WITH parent_id IS NULL 
                                CONNECT BY PRIOR id = parent_id 
                                ORDER SIBLINGS BY ord 
                                """ % app_id)
        modules = []
        for module in module_qs:
            row = {}
            row.update({'id':module.id})
            row.update({'code':module.code})
            row.update({'name':module.name})
            row.update({'status':module.status})
            row.update({'action':module.action})
            row.update({'icon_class':module.icon_class})
            row.update({'url':module.url})
            row.update({'create_date':module.create_date.strftime('%Y-%m-%d %H:%M:%S')})
            row.update({'user_name':module.user_name})
            row.update({'ord':module.ord})
#             type
            module_type = _(u"unknown")
            icon = None
            if module.type == "R":
                module_type = _(u"Cha")
                icon = '/images/module/home.png'
            elif module.type == "G":
                module_type = _(u"Nhóm module")
                icon = '/images/module/group.png'
            elif module.type == "M":
                module_type = _(u"Module")
                icon = '/images/module/module.png'
            elif module.type == "P":
                module_type = _(u"Quyền hạn")
                icon = '/images/module/permission.png'
            row.update({'module_type':module_type})
            row.update({'type':module.type})
            row.update({'icon':icon})
#             parent
            if module.parent is not None:
                row.update({'parent_id':module.parent.id})
                row.update({'parent_name':module.parent.name})
            else:
                row.update({'open':True,'iconOpen':'/images/module/home.png', 'iconClose':'/images/module/home.png'})
            modules.append(row)
        return HttpResponse(json.dumps({"handle":"success","modules":modules},cls=DateEncoder) ,content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({"handle":"error", "message": str(ex)}),content_type="application/json")