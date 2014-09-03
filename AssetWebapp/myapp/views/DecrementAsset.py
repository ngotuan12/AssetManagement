'''
Created on Apr 3, 2014

@author: TuanNA
'''
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.Dept import Dept
from myapp.models.StockAssetSerial import StockAssetSerial
from myapp.models.Stock import Stock


@login_required(login_url='/login')
@permission_required('myapp.view_decrement_asset',login_url='/permission-error')
def index(request):
	context = {}
	try:
		context.update({'depts':Dept.objects.all()})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("asset/decrement-asset.html", context,RequestContext(request))

@permission_required('myapp.view_decrement_asset',login_url='/permission-error')
def getListStock(request,dept_id):
	try:
		dept = Dept.objects.get(id=dept_id)
		stocks = Stock.objects.filter(dept=dept)
		infors =[]
		for stock in stocks:
			infors.append(model_to_dict(stock))
		return HttpResponse(json.dumps({'stocks':infors,}) ,content_type="application/json")
	except Exception as ex:
		return HttpResponse(json.dumps({"error": str(ex)}),content_type="application/json")	
@permission_required('myapp.view_decrement_asset',login_url='/permission-error')
def getListSerial(request,stock_id):
	try:
		stock = Stock.objects.get(id=stock_id)
		serials = StockAssetSerial.objects.filter(stock=stock)
		infors =[]
		for serial in serials:
			infors.append(model_to_dict(serial))
		return HttpResponse(json.dumps({'serials':infors}) ,content_type="application/json")
	except Exception as ex:
		return HttpResponse(json.dumps({"error": str(ex)}),content_type="application/json")	
