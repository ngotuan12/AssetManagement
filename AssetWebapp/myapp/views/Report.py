# -*- coding: utf-8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''

from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import requests

from myapp.models.List import List
from myapp.util import client
import xmlrpclib


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
		projects=List.objects.filter(list_type="7")
		context.update({"projects":projects})
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