'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models import Device
from myapp.models.Area import Area
from myapp.util import client


@login_required(login_url='/login')
@permission_required('myapp.view_device_report',login_url='/permission-error')
def view_device_report(request):
	context = {'devices':Device.objects.all().order_by("code","name","address"),'areas':Area.objects.filter(status="1").order_by("woodenleg","code")}
	if(request.POST) :
		device_id = request.POST["slDevice"]
		area_id = request.POST["slArea"]
		device_status = request.POST["slStatus"]
		authorization = client.getAuthorization()
		fileOut = client.exportDeviceReport(authorization,device_id,area_id,device_status)
		return HttpResponseRedirect('/report/'+fileOut)
	context.update(csrf(request))
	return render_to_response("report/device-report.html", context,RequestContext(request))
@login_required(login_url='/login')
@permission_required('myapp.view_device_detail_report',login_url='/permission-error')
def view_device_detail_report(request):
	context = {'devices':Device.objects.all().order_by("code","name","address"),'areas':Area.objects.filter(status="1").order_by("woodenleg","code")}
	if(request.POST) :
		device_id = request.POST["slDevice"]
		area_id = request.POST["slArea"]
		device_status = request.POST["slStatus"]
		authorization = client.getAuthorization()
		fileOut = client.exportDeviceDetailReport(authorization,device_id,area_id,device_status)
		return HttpResponseRedirect('/report/'+fileOut)
	context.update(csrf(request))
	return render_to_response("report/device-detail-report.html", context,RequestContext(request))
@login_required(login_url='/login')
@permission_required('myapp.view_device_error_report',login_url='/permission-error')
def view_device_error_report(request):
	context = {'devices':Device.objects.all().order_by("code","name","address"),'areas':Area.objects.filter(status="1").order_by("woodenleg","code")}
	if(request.POST) :
		device_id = request.POST["slDevice"]
		area_id = request.POST["slArea"]
		device_status = request.POST["slStatus"]
		authorization = client.getAuthorization()
		fileOut = client.exportDeviceErrorReport(authorization,device_id,area_id,device_status)
		return HttpResponseRedirect('/report/'+fileOut)
	context.update(csrf(request))
	return render_to_response("report/device-error-report.html", context,RequestContext(request))