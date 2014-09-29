# -*- coding: utf-8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''
import cx_Oracle
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.db import connection
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from myapp.models.Dept import Dept
from myapp.models.List import List
from myapp.models.Stock import Stock
from myapp.models.StockAssetSerial import StockAssetSerial
from myapp.util.DateEncoder import DateEncoder


@login_required(login_url='/login/')
@permission_required('myapp.decrement_asset',login_url='/permission-error/')
def index(request):
	context = {}
	try:
		reasons = List.objects.raw("""
									SELECT id, name, code
									FROM list
									WHERE CONNECT_BY_ISLEAF = 1 AND list_type = '5'
									START WITH parent_id = (SELECT id
									FROM list
									WHERE code = '20' AND list_type = '5')
									CONNECT BY PRIOR id = parent_id
									""")
		context.update({'depts':Dept.objects.all()})
		context.update({'reasons':reasons})
		if request.POST:
			# Get parameter
			dept_id = request.POST["slDept"]
			stock_id = request.POST["slStock"]
			serial = request.POST["slSerial"]
			asset_id = request.POST["txtAssetID"]
# 			CapitalAmount_id = request.POST["txtCapitalAmount"]
# 			OriginalAmount_id = request.POST["txtOriginalAmount"]
# 			RemainAmount_id = request.POST["txtRemainAmount"]
			reason_id = request.POST["slReason"]
			note = request.POST["txtNote"]
			decrement_date = request.POST["dtDecrementDate"]
			cursor = connection.cursor()
			cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'DD/MM/YYYY HH24:MI:SS.FF'")
			p_error = cursor.var(cx_Oracle.STRING).var
			cursor.callproc("pck_stock_trans.export_asset_serial",
						(
							# p_error
							p_error,
							# p_stock_id
							stock_id,
							# p_ie_stock_id
							None,
							# p_asset_id
							asset_id,
							# p_seria
							serial,
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
			if p_error.getvalue() is not None:
				raise Exception(p_error.getvalue())
			context.update({'has_success':_(u"Giảm tài sản thành công")})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("asset/decrement-asset.html", context,RequestContext(request))

@permission_required('myapp.view_decrement_asset',login_url='/permission-error/')
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
@permission_required('myapp.view_decrement_asset',login_url='/permission-error/')
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