# -*- coding: utf-8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''
import cx_Oracle
import json
from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.db import connection
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from myapp.models.ApDomain import ApDomain
from myapp.models.Asset import Asset
from myapp.models.Country import Country
from myapp.models.Dept import Dept
from myapp.models.List import List
from myapp.models.Stock import Stock
from myapp.models.StockAssetSerial import StockAssetSerial
from myapp.models.Supplier import Supplier


@login_required(login_url='/login/')
@permission_required('myapp.increment_asset', login_url='/permission-error/')
def index(request):
	context = {}
	try:
		assets = Asset.objects.raw("select id, NAME,code,parent_code "+
									"FROM asset "+ 
									"WHERE connect_by_isleaf = 1 "+
									"start with parent_id is null "+
									"connect by prior id = parent_id ORDER BY code ")
		reasons = List.objects.raw("""
									SELECT id, name, code
									FROM list
									WHERE CONNECT_BY_ISLEAF = 1 AND list_type = '5'
									START WITH parent_id = (SELECT id
									FROM list
									WHERE code = '10' AND list_type = '5')
									CONNECT BY PRIOR id = parent_id
									""")
		context.update({'assets':assets, 'reasons':reasons, 'methods':List.objects.filter(list_type='6'), 
					'capitals':List.objects.filter(list_type='3')})
		
		context.update({'countries':Country.objects.all()})
		context.update({'suppliers':Supplier.objects.all()})
		context.update({'depts':Dept.objects.all()})
		context.update({'stocks':Stock.objects.all()})
		context.update({'goals':List.objects.filter(list_type='2')})
		context.update({'states':List.objects.filter(list_type='4')})
		context.update({'projects':List.objects.filter(list_type='7')})
		context.update({'units':ApDomain.objects.filter(type='UNIT')})
		context.update({'sources':ApDomain.objects.filter(type='SOURCE')})
		context.update({'parents':StockAssetSerial.objects.filter(parent_serial__isnull=True)})
		if request.POST: 
			# Get parameter
			asset_id = request.POST["slAsset"]
			reason_id = request.POST["slReason"]
			method_id = request.POST["slMethod"]
			arr_capital_id = request.POST["hd_arr_capital"]
			arr_capital_code = request.POST["hd_arr_capital_code"]
			arr_capital_name = request.POST["hd_arr_capital_name"]
			country_id = request.POST["slCountry"]
			supplier_id = request.POST["slSupplier"]
			dept_id = request.POST["slDept"]
			stock_id = request.POST["slStock"]
			goal_id = request.POST["slGoal"]
			state_id = request.POST["slState"]
			buy_date = request.POST["dtBuyDate"]
			start_use_date = request.POST["dtStartUseDate"]
			up_date = request.POST["dtUpDate"]
			product_date = request.POST["dtProductDate"]
			atrophy_date = request.POST["dtAtrophyDate"]
			arr_origin_price = request.POST["hd_arr_original"]
			serial = request.POST["txtSerial"]
			arr_remain_amount = request.POST["hd_arr_remain"]
			note = request.POST["txtNote"]
			unit_code = request.POST["slUnit"]
			power = request.POST["txtPower"]
			source_code = request.POST["slSource"]
			decision_no = request.POST["txtDecisionNo"]
			asset_name = request.POST["txtAssetName"]
			document_status = request.POST["slDocumentStatus"]
			interval = request.POST["txtInterval"]
			parent_serial = None
			
			project_id = request.POST["slProject"]
			decision_date = request.POST["dtDecision"]
			quantity = request.POST["txtQuantity"]
			model = request.POST["txtModel"]
			product_seri = request.POST["txtProductSeri"]
			
			if request.POST.get("ckChildAsset"):
				parent_serial = request.POST["slParent"]
			cursor = connection.cursor()
			cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'DD/MM/YYYY HH24:MI:SS.FF'")
			p_error = cursor.var(cx_Oracle.STRING).var
			cursor.callproc("pck_stock_trans.import_asset_serial",
						(
							#p_error
							p_error,
							#p_stock_id
							stock_id,
							#p_ie_stock_id
							None,
							#p_asset_id
							asset_id,
							#p_serial
							serial,
							#p_arr_original_value
							arr_origin_price,
							#p_arr_remain_value
							arr_remain_amount,
							#p_import_date
							up_date,
							#p_use_date
							start_use_date,
							#p_state_id
							state_id,
							#p_goal_id
							goal_id,
							#p_country_id
							country_id,
							#p_supplier_id
							supplier_id,
							#p_arr_capital_id
							arr_capital_id,
							#p_amortize_id
							method_id,
							#p_reason_id
							reason_id,
							#p_dept_id
							dept_id,
							#p_staff_id
							None,
							#p_username
							request.user.username,
							#p_note
							note,
							#p_buy_date
							buy_date,
							#p_amortize_date
							atrophy_date,
							#p_project_id
							project_id,
							#p_unit
							unit_code,
							#p_product_date
							product_date,
							#p_power
							power,
							#p_source
							source_code,
							#p_decision_no
							decision_no,
							#p_document_status
							document_status,
							#p_name
							asset_name,
							#p_interval
							interval,
							#p_parent_serial
							parent_serial,
							#p_decision_date
							decision_date,
							#p_quantity
							quantity,
							#p_model
							model,
							#p_product_seri
							product_seri
						))
			cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")
			cursor.close()
			if p_error.getvalue() is not None:
				st =Stock.objects.get(id=stock_id)
				context.update({'asset_id':asset_id})
				context.update({'reason_id':reason_id})
				context.update({'method_id':method_id})
				context.update({'country_id':country_id})
				context.update({'supplier_id':supplier_id})
				context.update({'dept_id':dept_id})
				context.update({'stock':st})
				context.update({'goal_id':goal_id})
				context.update({'state_id':state_id})
				context.update({'buy_date':datetime.strptime(buy_date,'%d/%m/%Y')})
				context.update({'start_use_date':datetime.strptime(start_use_date,'%d/%m/%Y')})
				context.update({'up_date':datetime.strptime(up_date,'%d/%m/%Y')})
				context.update({'product_date':datetime.strptime(product_date,'%d/%m/%Y')})
				context.update({'atrophy_date':datetime.strptime(atrophy_date,'%d/%m/%Y')})
				context.update({'decision_date':datetime.strptime(decision_date,'%d/%m/%Y')})
				context.update({'arr_origin_price':arr_origin_price})
				context.update({'serial':serial})
				context.update({'note':note})
				context.update({'unit_code':unit_code})
				context.update({'power':power})
				context.update({'source_code':source_code})
				context.update({'decision_no':decision_no})
				context.update({'asset_name':asset_name})
				context.update({'document_status':document_status})
				context.update({'interval':interval})
				context.update({'project_id':project_id})
				context.update({'quantity':quantity})
				context.update({'model':model})
				context.update({'product_seri':product_seri})
				context.update({'parent_serial':parent_serial})
				
				context.update({'arr_capital_id':arr_capital_id})
				context.update({'arr_origin_price':arr_origin_price})
				context.update({'arr_remain_amount':arr_remain_amount})
				context.update({'arr_capital_code':arr_capital_code})
				context.update({'arr_capital_name':arr_capital_name})
				raise Exception(p_error.getvalue())
			context.update({'has_success':_(u"Thêm tài sản thành công")})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("asset/increment-asset.html", context, RequestContext(request))
def get_serial_no(request,day,month,year):
	try:
		dt_decision =day+"/"+month+"/"+year
		serialNo=""
		cursor = connection.cursor()
		cursor.execute("select (pck_import.get_serial_no(to_date('"+ dt_decision +"','dd/mm/yyyy'),5))serial from dual")
		row =cursor.fetchone()
		serialNo =row[0]
		cursor.close()
		return HttpResponse(json.dumps({'serialNo':serialNo,}) ,content_type="application/json")
	except Exception as ex:
		print(ex)
	return HttpResponse(json.dumps({"error": str(ex)}),content_type="application/json")
def get_interval(request,asset_id):
	try:
		interval=""
		cursor = connection.cursor()
		cursor.execute("SELECT get_interval_amortize("+ asset_id +",null) interval  FROM dual;")
		row =cursor.fetchone()
		interval =row[0]
		cursor.close()
		return HttpResponse(json.dumps({'interval':interval,}) ,content_type="application/json")
	except Exception as ex:
		print(ex)
	return HttpResponse(json.dumps({"error": str(ex)}),content_type="application/json")
