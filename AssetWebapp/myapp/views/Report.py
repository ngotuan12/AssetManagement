# -*- coding: utf-8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''
import json
import xmlrpclib

from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf, request
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import requests

from myapp.models.ApDomain import ApDomain
from myapp.models.Dept import Dept
from myapp.models.List import List
from myapp.models.StockAssetSerial import StockAssetSerial
from myapp.util import client
from myapp.util.DateEncoder import DateEncoder


@login_required(login_url='/login')
def view_reason_report(request):
	context = {}
	if request.POST :
		reason_code = request.POST['txtReasonCode']
		reason_name = request.POST['txtReasonName']
		reason_status = request.POST['optStatus']
		authorization = client.getAuthorization(request.user.username)
		params_object = {
							"p_reason_code":reason_code,
							"p_reason_name":reason_name,
							"p_reason_status":reason_status
						}
		fileOut = client.exportReportByJasper(authorization, request.user.username, "reason_list", params_object,"EXCEL")
		return HttpResponseRedirect('/report/' + fileOut)
	context.update(csrf(request))
	return render_to_response("report/reason-report.html", context, RequestContext(request))

@login_required(login_url='/login/')
@permission_required('myapp.summarize_inventorry_asset_report', login_url='/permission-error/')
def view_Asset_Inventory_report(request):
	try:
		context = {}
		capitals = List.objects.filter(list_type="3")
		context.update({'capitals':capitals})
		if request.POST :
			capital_id = request.POST['optCapital']
			authorization = client.getAuthorization(request.user.username)
			params_object = {
								"p_capital_id":capital_id
							}
			fileOut = client.exportReportByJasper(authorization, request.user.username, "RPTAssetInventory_Summarize", params_object,"EXCEL")
			return HttpResponseRedirect('/report/' + fileOut)
		context.update(csrf(request))
	except Exception as ex:
		context.update({'has_error':str(ex)})
	return render_to_response("report/report-verify-asset-summarize.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.inventory_asset_report', login_url='/permission-error/')
def verify_asset_report(request):
	context = {}
	try:
		capitals = List.objects.filter(list_type="3")
		statuses = List.objects.filter(list_type="4")
		context.update({'capitals':capitals,'statuses':statuses})
		if request.POST :
			capital_id = request.POST['optCapital']
			use_date = request.POST['dtUseDate']
			status = request.POST['optStatus']
			authorization = client.getAuthorization(request.user.username)
			params_object = {
								"p_capital_id":capital_id,
								"p_use_date":use_date,
								"p_status":status
							}
			fileOut = client.exportReportByJasper(authorization, request.user.username, "RPTAssetInventory", params_object,"EXCEL")
			return HttpResponseRedirect('/report/' + fileOut)
	except xmlrpclib.ProtocolError:
		context.update({'has_error':'Không kết nối được server report'})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	context.update(csrf(request))
	return render_to_response("report/report-verify-asset.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.asset_project_report', login_url='/permission-error/')
def asset_project_report(request):
	context={}
	try:
# 		projects=List.objects.filter(list_type="7")
		projects = List.objects.raw("SELECT a.id,a.name "+
									"FROM list a "+ 
									"WHERE a.list_type ='7'")
		lsProjects = []
		for project in projects:
			row = {}
			row.update({'id':project.id})
			row.update({'name':project.name})
			lsProjects.append(row)
		context.update({'data':json.dumps(lsProjects,cls=DateEncoder)})
# 		context.update({"projects":projects})
		if request.POST:
			project_id=request.POST['slProject']
			authorization = client.getAuthorization(request.user.username)
			fileOut = client.exportAssetByProjectReport(authorization, project_id, request.user.username)
			return HttpResponseRedirect('/report/' + fileOut)
	except xmlrpclib.ProtocolError:
		context.update({'has_error':'Không kết nối được server report'})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	context.update(csrf(request))
	return render_to_response("report/report-asset-by-project.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.asset_project_report', login_url='/permission-error/')
def asset_amortization_report(request):
	context={}
	try:
		depts =Dept.objects.all()
		dept_default =ApDomain.objects.get(type='PROVINCE',code='CODE')
		context.update({'depts':depts,'dept_default':dept_default})
		if request.POST:
			dept_id = ''
			if request.POST['slDept']:
				dept_id=request.POST['slDept']
				dept_name =request.POST['hd_dept_name']
			report_name =request.POST['slReportName']
			from_date = request.POST["dtFromDate"]
			to_date = request.POST["dtToDate"]
			arrFromDate = from_date.split('/')
			arrTomDate = to_date.split('/')
			from_date_default ="01"+"/"+arrFromDate[1]+"/"+arrFromDate[2]
			to_date_default ="01"+"/"+arrTomDate[1]+"/"+arrTomDate[2]
			authorization = client.getAuthorization(request.user.username)
			params_object_default = {
								"p_from_date":from_date_default,
								"p_to_date":to_date_default,
								"p_dept_id":dept_id,
								"p_dept_name":dept_name
							}
			params_object = {
								"p_from_date":from_date,
								"p_to_date":to_date,
								"p_dept_id":dept_id,
								"p_dept_name":dept_name
							}
			#if report_name=="RPTAssetAmortization":
			#fileOut = client.exportReportByJasper(authorization, request.user.username, report_name, params_object_default,"PDF")
			#else:
			fileOut = client.exportReportByJasper(authorization, request.user.username, report_name, params_object,"EXCEL")
			return HttpResponseRedirect('/report/' + fileOut)
	except xmlrpclib.ProtocolError:
		context.update({'has_error':'Không kết nối được server report'})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	context.update(csrf(request))
	return render_to_response("report/report-amortization.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.asset_project_report', login_url='/permission-error/')
def asset_sum_amortization_report(request):
	context={}
	try:
		depts =Dept.objects.all()
		dept_default =ApDomain.objects.get(type='PROVINCE',code='CODE')
		context.update({'depts':depts,'dept_default':dept_default})
		if request.POST:
			dept_id = ''
			if request.POST['slDept']:
				dept_id=request.POST['slDept']
				dept_name =request.POST['hd_dept_name']
			from_date = request.POST["dtFromDate"]
			to_date = request.POST["dtToDate"]
			arrFromDate = from_date.split('/')
			arrTomDate = to_date.split('/')
			from_date ="01"+"/"+arrFromDate[1]+"/"+arrFromDate[2]
			to_date ="01"+"/"+arrTomDate[1]+"/"+arrTomDate[2]
			authorization = client.getAuthorization(request.user.username)
			params_object = {
								"p_from_date":from_date,
								"p_to_date":to_date,
								"p_dept_id":dept_id,
								"p_dept_name":dept_name
							}
			fileOut = client.exportReportByJasper(authorization, request.user.username, "RPTAssetAmortizationSum", params_object,"PDF")
			return HttpResponseRedirect('/report/' + fileOut)
	except xmlrpclib.ProtocolError:
		context.update({'has_error':'Không kết nối được server report'})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	context.update(csrf(request))
	return render_to_response("report/report-sum-amortization.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.asset_project_report', login_url='/permission-error/')
def asset_change_report(request):
	context={}
	try:
		depts =Dept.objects.all()
		dept_default =ApDomain.objects.get(type='PROVINCE',code='CODE')
		context.update({'depts':depts,'dept_default':dept_default})
		if request.POST:
			dept_id = ''
			dept_name = '-1'
			if request.POST['slDept']:
				dept_id=request.POST['slDept']
				dept_name =request.POST['hd_dept_name']
			from_date = request.POST["dtFromDate"]
			to_date = request.POST["dtToDate"]
# 			arrFromDate = from_date.split('/')
# 			arrTomDate = to_date.split('/')
# 			from_date ="01"+"/"+arrFromDate[1]+"/"+arrFromDate[2]
# 			to_date ="01"+"/"+arrTomDate[1]+"/"+arrTomDate[2]
			authorization = client.getAuthorization(request.user.username)
			params_object = {
								"p_from_date":from_date,
								"p_to_date":to_date,
								"p_dept_id":dept_id,
								"p_dept_name":dept_name
							}
			fileOut = client.exportReportByJasper(authorization, request.user.username, "RPTAssetChange", params_object,"PDF")
			return HttpResponseRedirect('/report/' + fileOut)
	except xmlrpclib.ProtocolError:
		context.update({'has_error':'Không kết nối được server report'})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	context.update(csrf(request))
	return render_to_response("report/report-change-asset.html", context, RequestContext(request))
def asset_daily_report(request):
	context={}
	try:
		depts =Dept.objects.all()
		context.update({'depts':depts})
		if request.POST:
			dept_id = ''
			dept_name = '-1'
			if request.POST['slDept']:
				dept_id=request.POST['slDept']
				dept_name =request.POST['hd_dept_name']
			from_date = request.POST["dtFromDate"]
#			to_date = request.POST["dtToDate"]
# 			arrFromDate = from_date.split('/')
# 			arrTomDate = to_date.split('/')
# 			from_date ="01"+"/"+arrFromDate[1]+"/"+arrFromDate[2]
# 			to_date ="01"+"/"+arrTomDate[1]+"/"+arrTomDate[2]
			authorization = client.getAuthorization(request.user.username)
			params_object = {
								"p_date":from_date,								
								"p_dept_id":dept_id,
								"p_dept_name":dept_name
							}
			fileOut = client.exportReportByJasper(authorization, request.user.username, "rp_hientrang", params_object,"EXCEL")
			return HttpResponseRedirect('/report/' + fileOut)
	except xmlrpclib.ProtocolError:
		context.update({'has_error':'Không kết nối được server report'})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	context.update(csrf(request))
	return render_to_response("report/report-daily-asset.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.asset_project_report', login_url='/permission-error/')
def card_asset(request):
	context={}
	try:
		ls_stock_asset_serials =StockAssetSerial.objects.filter(num_sub =0)
		stock_asset_serials=[]
		for st in ls_stock_asset_serials:
			row = {}
			row.update({'id':st.id})
			row.update({'name':st.name})
			row.update({'serial':st.serial})
			stock_asset_serials.append(row)
		context.update({'data':json.dumps(stock_asset_serials,cls=DateEncoder)})
		if request.POST:
			stock_asset_id=request.POST['slSerial'].strip()
			authorization = client.getAuthorization(request.user.username)
			if str(stock_asset_id) == '-1':
				for stock_asset_serials in ls_stock_asset_serials:
					params_object = {
								"p_stock_serial_id":str(stock_asset_serials.id)
							}
					client.exportReportByJasper(authorization, request.user.username, "RPTAssetSerial", params_object,"PDF")
			else:
				params_object = {
								"p_stock_serial_id":stock_asset_id
							}
				client.exportReportByJasper(authorization, request.user.username, "RPTAssetSerial", params_object,"PDF")
# 			return HttpResponseRedirect('/report/' + fileOut)
	except xmlrpclib.ProtocolError:
		context.update({'has_error':'Không kết nối được server report'})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	context.update(csrf(request))
	return render_to_response("report/card-asset.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.asset_project_report', login_url='/permission-error/')
def asset_fix_report(request):
	context={}
	try:
		depts =Dept.objects.all()
		dept_default =ApDomain.objects.get(type='PROVINCE',code='CODE')
		context.update({'depts':depts,'dept_default':dept_default})
		if request.POST:
			dept_id = ''
			if request.POST['slDept']:
				dept_id=request.POST['slDept']
				dept_name =request.POST['hd_dept_name']
			report_name =request.POST['slReportName']
			from_date = request.POST["dtFromDate"]
			to_date = request.POST["dtToDate"]
			authorization = client.getAuthorization(request.user.username)
			type_extension =""
			params_object = {
								"p_from_date":from_date,
								"p_to_date":to_date,
								"p_dept_id":dept_id,
								"p_dept_name":dept_name
							}
			if report_name=="RPTAssetAmortization":
				type_extension="PDF"
			else:
				type_extension="EXCEL"
			fileOut = client.exportReportByJasper(authorization, request.user.username, report_name, params_object,type_extension)
			return HttpResponseRedirect('/report/' + fileOut)
	except xmlrpclib.ProtocolError:
		context.update({'has_error':'Không kết nối được server report'})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	context.update(csrf(request))
	return render_to_response("report/report-fix.html", context, RequestContext(request))