# -*- coding: utf-8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''
import cx_Oracle
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.db import connection
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.List import List
from myapp.models.StockAssetSerial import StockAssetSerial
from myapp.models.Staff import Staff

@login_required(login_url='/login/')
def index(request):
	context = {}
	try:
		serials = StockAssetSerial.objects.all()
		context.update({'serials':serials})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("asset/verify-asset.html", context,RequestContext(request))
def verify(request,serial_id):
	context = {}
	try:
		serial = StockAssetSerial.objects.get(id=serial_id)
		state =serial.state.id
		context.update({'serial':serial,'state':state})
		context.update({'states':List.objects.filter(list_type='4')})
		context.update({'staffs':Staff.objects.all()})
		if(request.POST):
			remain_amount = request.POST["txtRemainAmount"]
			state_id = request.POST["slState"]
			check_no = request.POST["txtCheckNo"]
			staff_code = request.POST["slStaff"]
			note = request.POST["txtNote"]
			username = request.user.username
			dtVerify = request.POST["dtVerify"]
			p_serial = serial.serial
			p_error  = ''
			cursor = connection.cursor()
			cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'DD/MM/YYYY HH24:MI:SS.FF'")
			p_error = cursor.var(cx_Oracle.STRING).var
			cursor.callproc("pck_asset.check_asset",
						(
							#p_error
							p_error,
							#p_check_no
							check_no,
							#p_check_user
							staff_code,
							#p_serial
							p_serial,
							#p_remain_amount
							remain_amount,
							#p_interval
							None,
							#p_state_id
							state_id,
							#p_note
							note,
							#p_username
							username,
							#p_check_date
							dtVerify
						))
			cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")
			cursor.close()
			if p_error.getvalue() is not None:
				raise Exception(p_error.getvalue())
			context.update({'has_success':"Giao dịch thành công"})
			return HttpResponseRedirect("/verify-asset/")
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("asset/verify-asset-edit.html", context,RequestContext(request))