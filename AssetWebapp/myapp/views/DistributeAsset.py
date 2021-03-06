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
from django.http.response import  HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from myapp.models.CapitalValue import CapitalValue
from myapp.models.Dept import Dept
from myapp.models.List import List
from myapp.models.StockAssetSerial import StockAssetSerial
from myapp.util.DateEncoder import DateEncoder


@login_required(login_url='/login/')
@permission_required('myapp.verify_asset', login_url='/permission-error/')
def index(request):
	context = {}
	isPost =False
	try:
		serials = StockAssetSerial.objects.raw("SELECT a.id,a.name,a.serial,a.quantity,b.name project_name "+
									"FROM stock_asset_serial a,list b "+ 
									"WHERE a.project_id =b.id AND a.num_sub = 0 ")
		
		stock_asset_serials = []
		for serial in serials:
			row = {}
			row.update({'id':serial.id})
			row.update({'name':serial.name})
			row.update({'serial':serial.serial})
			row.update({'quantity':serial.quantity})
			row.update({'project_name':serial.project_name})
			stock_asset_serials.append(row)
		context.update({'data':json.dumps(stock_asset_serials,cls=DateEncoder)})
		context.update({'states':List.objects.filter(list_type='4')})
		context.update({'depts':Dept.objects.all()})
		if(request.POST):
			isPost =True
			sucess =True
			lsDeptId = request.POST["hd_ls_dept_id"]
			asset_serial_id = request.POST["hd_parent_stock_asset_id"]
			arrDeptId = lsDeptId.split(',')
			username = request.user.username
			
			for d in arrDeptId :
				deptId = d
				name = request.POST["txtName"+deptId]
				serial = request.POST["txtSerial"+deptId]
				asset_quantity  = request.POST["txtQuantity"+deptId]
				note =request.POST["txtNote"+deptId]
				arrRemainValue = request.POST["txtRemain"+deptId]
				arrOriginalValue = request.POST["txtOriginal"+deptId]
				arrCapital = request.POST["txtCapital"+deptId]
				
# 				print("asset_serial_id: "+asset_serial_id)
# 				print("deptId: "+deptId)
# 				print("name: "+name)
# 				print("serial: "+serial)
# 				print("note: "+note)
# 				print("arrRemainValue: "+arrRemainValue)
# 				print("arrOriginalValue: "+arrOriginalValue)
# 				print("arrCapital: "+arrCapital)
# 				print("")
				p_error  = ''
				cursor = connection.cursor()
				cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS' "  
	                                       "NLS_TIMESTAMP_FORMAT = 'DD/MM/YYYY HH24:MI:SS.FF'")
				p_error = cursor.var(cx_Oracle.STRING).var
				cursor.callproc("pck_stock_trans.distribute_capital",
							(
								#p_error
								p_error,
								#p_asset_serial_id
								asset_serial_id,
								#p_dept_id
								deptId,
								#p_stock_id
								None,
								#p_name
								name,
								#p_serial
								serial,
								#p_quantity
								asset_quantity,
								#p_arr_capital
								arrCapital,
								#p_arr_original_value
								arrOriginalValue,
								#p_arr_remain_value
								arrRemainValue,
								#p_description
								note,
								#p_username
								username
							))
				cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' "  
	                                       "NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")
				cursor.close()
				if p_error.getvalue() is not None:
					sucess =False
					raise Exception(p_error.getvalue())
			context.update({'has_success':_(u"Giao dịch thành công")})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		if isPost == True and sucess == True :
			return HttpResponseRedirect('/view-distribute-asset/'+ asset_serial_id + '/')
		else:
			return render_to_response("asset/distribute-asset.html", context,RequestContext(request))
@login_required(login_url='/login/')
def view_distribute_asset(request,stock_asset_serial_id):
	context = {}
	try:
		stock_asset = StockAssetSerial.objects.get(id =stock_asset_serial_id)
		capital_value_parent = CapitalValue.objects.filter(stock_asset_serial =stock_asset_serial_id)
		lsStock_asset_child = StockAssetSerial.objects.filter(parent_serial = stock_asset.serial)
		lsCapital_value_child =CapitalValue.objects.filter(stock_asset_serial__in =lsStock_asset_child)
		context.update({'stock_asset':stock_asset})
		context.update({'capital_value_parent':capital_value_parent})
		context.update({'lsCapital_value_child':lsCapital_value_child})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("asset/view-distribute-asset.html", context,RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.verify_asset_edit', login_url='/permission-error/')
def get_capital(request,asset_id):
	try:
		capitals_qs = List.objects.raw("""
                                SELECT a.id, a.stock_asset_serial_id, a.capital_id,b.name,b.code, a.original_value,
                                    a.remain_value, a.description 
                                FROM capital_value a,list b 
                                WHERE a.capital_id = b.id AND a.stock_asset_serial_id="""+asset_id+"""
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