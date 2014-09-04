'''
Created on Apr 3, 2014

@author: TuanNA
'''
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.db import connection
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.Dept import Dept
from myapp.models.Reason import Reason
from myapp.models.Stock import Stock
from myapp.models.StockAssetSerial import StockAssetSerial
from myapp.util.DateEncoder import DateEncoder


@login_required(login_url='/login')
@permission_required('myapp.view_decrement_asset',login_url='/permission-error')
def index(request):
	context = {}
	try:
		context.update({'depts':Dept.objects.all()})
		context.update({'reasons':Reason.objects.filter(group_code = '2')})
		if request.POST: 
			# Get parameter
			dept_id = request.POST["slDept"]
			stock_id = request.POST["slStock"]
			serial_id = request.POST["slSerial"]
# 			CapitalAmount_id = request.POST["txtCapitalAmount"]
# 			OriginalAmount_id = request.POST["txtOriginalAmount"]
# 			RemainAmount_id = request.POST["txtRemainAmount"]
			reason_id = request.POST["slReason"]
			note = request.POST["txtNote"]
			decrement_date = request.POST["dtDecrementDate"]
			p_error  = ''
			cursor = connection.cursor()
			cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'DD/MM/YYYY HH24:MI:SS.FF'")
			cursor.callproc("pck_stock_trans.export_stock_asset_serial",
						(
							# p_error
							p_error,
							# p_stock_id
							stock_id,
							# p_ie_stock_id
							None,
							# p_asset_id
							None,
							# p_seria
							serial_id,
							# p_export_date
							decrement_date,
							# p_reason_id
							reason_id,
							# p_dept_id
							dept_id,
							# p_staff_id
							None,
							# p_username
							request.user.username,
							# p_note	
							note						
						))
			cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")
			cursor.close()
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
		return HttpResponse(json.dumps({'serials':infors},cls=DateEncoder) ,content_type="application/json")
	except Exception as ex:
		return HttpResponse(json.dumps({"error": str(ex)}),content_type="application/json")	
