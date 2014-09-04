'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models import Device
from myapp.models.Area import Area
from myapp.util import client
from myapp.models.List import List


# @login_required(login_url='/login')
# @permission_required('myapp.view_device_report',login_url='/permission-error')
# def view_device_report(request):
# 	context = {'devices':Device.objects.all().order_by("code","name","address"),'areas':Area.objects.filter(status="1").order_by("woodenleg","code")}
# 	if(request.POST) :
# 		device_id = request.POST["slDevice"]
# 		area_id = request.POST["slArea"]
# 		device_status = request.POST["slStatus"]
# 		authorization = client.getAuthorization()
# 		fileOut = client.exportDeviceReport(authorization,device_id,area_id,device_status)
# 		return HttpResponseRedirect('/report/'+fileOut)
# 	context.update(csrf(request))
# 	return render_to_response("report/device-report.html", context,RequestContext(request))
# @login_required(login_url='/login')
# @permission_required('myapp.view_device_detail_report',login_url='/permission-error')
# def view_device_detail_report(request):
# 	context = {'devices':Device.objects.all().order_by("code","name","address"),'areas':Area.objects.filter(status="1").order_by("woodenleg","code")}
# 	if(request.POST) :
# 		device_id = request.POST["slDevice"]
# 		area_id = request.POST["slArea"]
# 		device_status = request.POST["slStatus"]
# 		authorization = client.getAuthorization()
# 		fileOut = client.exportDeviceDetailReport(authorization,device_id,area_id,device_status)
# 		return HttpResponseRedirect('/report/'+fileOut)
# 	context.update(csrf(request))
# 	return render_to_response("report/device-detail-report.html", context,RequestContext(request))
# @login_required(login_url='/login')
# @permission_required('myapp.view_device_error_report',login_url='/permission-error')
# def view_device_error_report(request):
# 	context = {'devices':Device.objects.all().order_by("code","name","address"),'areas':Area.objects.filter(status="1").order_by("woodenleg","code")}
# 	if(request.POST) :
# 		device_id = request.POST["slDevice"]
# 		area_id = request.POST["slArea"]
# 		device_status = request.POST["slStatus"]
# 		authorization = client.getAuthorization()
# 		fileOut = client.exportDeviceErrorReport(authorization,device_id,area_id,device_status)
# 		return HttpResponseRedirect('/report/'+fileOut)
# 	context.update(csrf(request))
# 	return render_to_response("report/device-error-report.html", context,RequestContext(request))
@login_required(login_url='/login')
#@permission_required('myapp.view_reason_report', login_url='/permission-error')
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

@login_required(login_url='/login')
#@permission_required('myapp.view_Asset_Inventory_report', login_url='/permission-error')
def view_Asset_Inventory_report(request):
	
	
	capitals = List.objects.filter(list_type="3")
	statuses = List.objects.filter(list_type="4")
	context = {'capitals':capitals,'statuses':statuses}
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
	context.update(csrf(request))
	return render_to_response("report/asset-inventory-report.html", context, RequestContext(request))

