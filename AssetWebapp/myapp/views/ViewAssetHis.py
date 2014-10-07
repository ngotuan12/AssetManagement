# -*- coding: utf-8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.StockAssetSerial import StockAssetSerial
from myapp.models.StockAssetSerialHis import StockAssetSerialHis


@login_required(login_url='/login/')
@permission_required('myapp.edit_increment_asset', login_url='/permission-error/')
def index(request,serial):
	context = {}
	try:
		stockAssetSerial = StockAssetSerial.objects.get(serial=serial)
		stockAssetSerials = StockAssetSerialHis.objects.filter(serial=serial)
		context.update({'stockAssetSerials':stockAssetSerials ,'stockAssetSerial' : stockAssetSerial})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("asset/view-asset-his.html", context, RequestContext(request))