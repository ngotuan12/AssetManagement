# -*- coding: utf-8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''
from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response, resolve_url
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from myapp.models.List import List
from myapp.models.Staff import Staff
from myapp.models.Supplier import Supplier


@login_required(login_url='/login/')
@permission_required('myapp.view_area', login_url='/permission-erro/r')
def index(request):
	context = {}
	try:
		suppliers = Supplier.objects.all().order_by('create_datetime')
		staffs = Staff.objects.all().order_by('create_datetime')
		context.update({'suppliers':suppliers,'staffs':staffs})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("supplier/list-supplier.html", context, RequestContext(request))
def edit_supplier(request,supplier_id):
	try:
		context = {}
		supplier = Supplier.objects.get(id = supplier_id)
		staffs = Staff.objects.all().order_by('create_datetime')
		context.update({"supplier":supplier,"staffs":staffs}) 
		if request.POST :
			try:
				supplier_code = request.POST['txtCode']
				supplier_name = request.POST['txtName']
				supplier_address = request.POST['txtAddress']
				supplier_createDate = datetime.strptime(request.POST['dt_supplier'],'%d/%M/%Y')
				supplier_phone = request.POST['txtPhone']
				supplier_fax = request.POST['txtFax']
				supplier_contact = request.POST['slContactPerson']
				supplier_status = request.POST['slStatus']
				
				supplier.code = supplier_code
				supplier.name = supplier_name
				supplier.address = supplier_address
				supplier.create_datetime = supplier_createDate
				supplier.tel = supplier_phone
				supplier.fax = supplier_fax
				supplier.contact_person = supplier_contact
				supplier.status = supplier_status
				check_supplier=Supplier.objects.exclude(id = supplier_id).filter(code=supplier_code)
				if(len(check_supplier) > 0):
					context.update({'has_error':_(u'Mã nhà sản xuất đã tồn tại')})
				else:
					supplier.save()
					return HttpResponseRedirect(resolve_url("supplier"))
			except Exception as ex:
				context.update({'has_error':ex})
		context.update(csrf(request))
		return render_to_response("supplier/edit-supplier.html",context, RequestContext(request))
	except List.DoesNotExist:
		return HttpResponseRedirect("/notfound-error")
def add_supplier(request):
	try:
		context = {}
		staffs = Staff.objects.all().order_by('create_datetime')
		context.update({"staffs":staffs}) 
		if request.POST :
			try:
				supplier_code = request.POST['txtCode']
				supplier_name = request.POST['txtName']
				supplier_address = request.POST['txtAddress']
				supplier_createDate = datetime.strptime(request.POST['dt_supplier'],'%d/%M/%Y')
				supplier_phone = request.POST['txtPhone']
				supplier_fax = request.POST['txtFax']
				supplier_contact = request.POST['slContactPerson']
				supplier_status = request.POST['slStatus']
				
				supplier = Supplier()
				supplier.code = supplier_code
				supplier.name = supplier_name
				supplier.address = supplier_address
				supplier.create_datetime = supplier_createDate
				supplier.tel = supplier_phone
				supplier.fax = supplier_fax
				supplier.contact_person = supplier_contact
				supplier.status = supplier_status
				check_supplier=Supplier.objects.filter(code=supplier_code)
				if(len(check_supplier) > 0):
					context.update({'has_error':_(u'Mã nhà sản xuất đã tồn tại')})
					context.update({'supplier':supplier})
				else:
					supplier.save()
					return HttpResponseRedirect(resolve_url("supplier"))
			except Exception as ex:
				context.update({'has_error':ex})
		context.update(csrf(request))
		return render_to_response("supplier/add-supplier.html",context, RequestContext(request))
	except List.DoesNotExist:
		return HttpResponseRedirect("/notfound-error")
@login_required(login_url='/login/')
def delete_supplier(request,supplier_id):
	try:
		supplier = Supplier.objects.get(id=supplier_id)
		supplier.delete()
		return HttpResponseRedirect(resolve_url("supplier"))
	except List.DoesNotExist:
			return HttpResponseRedirect("/notfound-error")