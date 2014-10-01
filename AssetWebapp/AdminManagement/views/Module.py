# -*- coding: utf-8 -*-
'''
Created on Sep 18, 2014

@author: TuanNA
@version: 1.0

'''
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.context_processors import csrf
from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response, resolve_url
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_http_methods

from AdminManagement.models.App import App
from AdminManagement.models.Module import Module
from myapp.util.DateEncoder import DateEncoder


@login_required(login_url='/login/')
@permission_required('admin.view_module',login_url='/permission-error/')
def index(request):
	context = {}
	try:
		app_id = "1"
		if request.GET.get("app_id"):
			app_id = request.GET.get("app_id")
		context.update({'app_id':app_id})
		context.update({'apps':App.objects.all()})
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
# 			type
			module_type = _(u"unknown")
			icon = None
			if module.type == "R":
				module_type = _(u"Cha")
				icon = '/images/module/home.png'
			elif module.type == "G":
				module_type = _(u"Nhóm chức năng")
				icon = '/images/module/group.png'
			elif module.type == "M":
				module_type = _(u"Chức năng")
				icon = '/images/module/module.png'
			elif module.type == "P":
				module_type = _(u"Quyền hạn")
				icon = '/images/module/permission.png'
			row.update({'module_type':module_type})
			row.update({'type':module.type})
			row.update({'icon':icon})
# 			parent
			if module.parent is not None:
				row.update({'parent_id':module.parent.id})
				row.update({'parent_name':module.parent.name})
			else:
				row.update({'open':True,'iconOpen':'/images/module/home.png', 'iconClose':'/images/module/home.png'})
			modules.append(row)
		context.update({'data':json.dumps(modules,cls=DateEncoder)})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
	return render_to_response("admin/module/module.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('admin.add_module',login_url='/permission-error/')
def add_group(request,parent_id):
	return on_add_module(request,"G",parent_id)
@login_required(login_url='/login/')
@permission_required('admin.add_module',login_url='/permission-error/')	
def add_module(request,parent_id):
	return on_add_module(request,"M",parent_id)
@login_required(login_url='/login/')
@permission_required('admin.add_module',login_url='/permission-error/')
def add_permission(request,parent_id):
	return on_add_module(request,"P",parent_id)
def on_add_module(request,module_type,parent_id):
	context = {}
	try:
		parent = Module.objects.get(id=parent_id)
		context.update({'parent_name':parent.name})
		context.update({'app_name':parent.app.name})
		# title
		title = ""
		if module_type=="G":
			title = _(u"THÊM NHÓM CHỨC NĂNG")
		elif module_type=="M":
			title = _(u"THÊM CHỨC NĂNG")
		elif module_type=="P":
			title = _(u"THÊM QUYỀN")
		context.update({'title':title})
		if request.POST:
			#auto commit
			transaction.set_autocommit(False)
			#parameter
			code = request.POST["txtCode"]
			name = request.POST["txtName"]
			action = request.POST["txtAction"]
			url = request.POST["txtUrl"]
			icon = request.POST["txtIcon"]
			ord_num = request.POST["txtOrd"]
			#new Module
			module = Module()
			module.code = code
			module.name = name
			module.action = action
			module.url = url
			module.type = module_type
			module.icon_class = icon
			module.ord = ord_num
			if request.POST.get('ckStatus'):
				module.status = "1"
			else:
				module.status = "0"
			module.parent = parent
			module.app = parent.app
			module.user_name = request.user.username
			if module_type=="M":
				#Insert content type
				content_type = ContentType()
				content_type.app_label = parent.app.code
				content_type.model = code
				content_type.name = name
				content_type.save()
				module.content_type = content_type
			elif module_type=="P":
				#Insert permission
				permission = Permission()
				permission.content_type = parent.content_type
				permission.name = name
				permission.codename = code
				permission.save()
				module.permission = permission
			#save module
			module.save()
			#commit
			transaction.commit()
			return HttpResponseRedirect(str("%s?app_id="+str(parent.app.id)) % resolve_url("module"))
	except Exception as ex:
		transaction.rollback()
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
	return render_to_response("admin/module/add-module.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('admin.edit_module',login_url='/permission-error/')
def edit_module(request,module_id):
	context = {}
	try:
		module = Module.objects.get(id=module_id)
		context.update({'parent_name':module.parent.name})
		context.update({'app_name':module.app.name})
		context.update({'module':module})
		if request.POST:
			#auto commit
			transaction.set_autocommit(False)
			#parameter
			code = request.POST["txtCode"]
			name = request.POST["txtName"]
			action = request.POST["txtAction"]
			url = request.POST["txtUrl"]
			icon = request.POST["txtIcon"]
			ord_num = request.POST["txtOrd"]
			#new Module
			module.code = code
			module.name = name
			module.action = action
			module.url = url
			module.icon_class = icon
			module.ord = ord_num
			if request.POST.get('ckStatus'):
				module.status = "1"
			else:
				module.status = "0"
			if module.type == "M":
				#Insert content type
				module.content_type.model = code
				module.content_type.name = name
				module.content_type.save()
			elif module.type=="P":
				#Insert permission
				module.permission.name = name
				module.permission.codename = code
				module.permission.save()
			#save module
			module.save()
			#commit
			transaction.commit()
			return HttpResponseRedirect(str("%s?app_id="+str(module.app.id)) % resolve_url("module"))
	except Exception as ex:
		transaction.rollback()
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
	return render_to_response("admin/module/edit-module.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('admin.delete_module',login_url='/permission-error/')
@require_http_methods(["POST",])
def delete_module(request,module_id):
	try:
		module = Module.objects.get(id=module_id)
		if request.POST :
			transaction.set_autocommit(False)
			if module.type == "M":
				module.content_type.delete()
			elif module.type=="P":
				module.permission.delete()
			module.delete();
			transaction.commit()
			return HttpResponseRedirect(str("%s?app_id="+str(module.app.id)) % resolve_url("module"))
	except Exception as ex:
		transaction.rollback()
		return HttpResponseRedirect("%s?error=%s" % (resolve_url("error-page"),str(ex)))