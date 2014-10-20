# -*- coding: utf-8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''
import json

import cx_Oracle
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.db import connection
from django.forms.models import model_to_dict
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, resolve_url
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from myapp.models.CapitalValue import CapitalValue
from myapp.models.Dept import Dept
from myapp.models.List import List
from myapp.models.Staff import Staff
from myapp.models.StockAssetSerial import StockAssetSerial


@login_required(login_url='/login/')
@permission_required('myapp.verify_asset', login_url='/permission-error/')
def index(request):
	context = {}
	try:
		if(request.POST):
			slSerial = request.POST["hd_ls_serial"]
			arrSerial = slSerial.split(',')
			for s in arrSerial:
				serial = s
				remain_amount = request.POST["txtRemain"+serial]
				
				state_id = request.POST["txtState"+serial]
				check_no = request.POST["txtCheckNo"+serial]
				staff_code = request.POST["txtStaff"+serial]
				note = request.POST["txtNote"+serial]
				username = request.user.username
				dtVerify = request.POST["txtDtVerify"+serial]
				p_serial = serial
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
			context.update({'has_success':_(u"Giao dịch thành công")})
		serials = StockAssetSerial.objects.all()
		
		context.update({'serials':serials})
		context.update({'states':List.objects.filter(list_type='4')})
		context.update({'depts':Dept.objects.all()})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("asset/profile-asset.html", context,RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.verify_asset_edit', login_url='/permission-error/')
def get_capital(request,asset_id):
	try:
		capitals_qs = List.objects.raw("""
                                SELECT a.id, a.stock_asset_serial_id, a.capital_id,b.name,b.code, a.original_value,
                                    a.remain_value, a.description 
                                FROM capital_value a,list b 
                                WHERE a.capital_id = b.id AND stock_asset_serial_id="""+asset_id+"""
                                """)
		capitals = []
		for capital in capitals_qs:
			row = {}
			row.update({'id':capital.id})
			row.update({'capital_id':capital.capital_id})
			row.update({'code':capital.code})
			row.update({'name':capital.name})
			row.update({'original_value':str(capital.original_value)})
			row.update({'remain_value':str(capital.remain_value)})
			capitals.append(row)
		return HttpResponse(json.dumps({'capitals':capitals,}) ,content_type="application/json")
	except Exception as ex:
		print(ex)
		return HttpResponse(json.dumps({"error": str(ex)}),content_type="application/json")