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
from django.utils.translation import ugettext as _

from myapp.models.ApDomain import ApDomain
from myapp.models.Asset import Asset
from myapp.models.Country import Country
from myapp.models.Dept import Dept
from myapp.models.List import List
from myapp.models.Reason import Reason
from myapp.models.Stock import Stock
from myapp.models.StockAssetSerial import StockAssetSerial
from myapp.models.Supplier import Supplier
from myapp.models.CapitalValue import CapitalValue

@login_required(login_url='/login/')
@permission_required('myapp.edit_increment_asset', login_url='/permission-error/')
def index(request,asset_id):
	context = {}
	try:
		stockAssetSerial = StockAssetSerial.objects.get(id=asset_id)
		capital_values = CapitalValue.objects.filter(stock_asset_serial =asset_id)
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
		
		context.update({'stockAssetSerial':stockAssetSerial})
		context.update({'capital_values':capital_values})
		context.update({'countries':Country.objects.all()})
		#context.update({'suppliers':Supplier.objects.all()})
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
			stock_asset_serial_id = request.POST["hd_stock_asset_serial_id"]
			asset_id = request.POST["slAsset"]
			reason_id = request.POST["slReason"]
			method_id = request.POST["slMethod"]
			arr_capital_id = request.POST["hd_arr_capital"]
			country_id = request.POST["slCountry"]
			supplier_id = request.POST["txtSupplier"]
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
				
# 			cursor = connection.cursor()
# 			cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS' "  
#                                        "NLS_TIMESTAMP_FORMAT = 'DD/MM/YYYY HH24:MI:SS.FF'")
# 			p_error = cursor.var(cx_Oracle.STRING).var
# 			cursor.callproc("pck_stock_trans.update_asset_serial",
# 						(
# 							#p_error
# 							p_error,
# 							#p_stock_serial_id
# 							stock_asset_serial_id,
# 							#p_stock_id
# 							stock_id,
# 							#p_ie_stock_id
# 							None,
# 							#p_asset_id
# 							asset_id,
# 							#p_serial
# 							serial,
# 							#p_arr_original_value
# 							arr_origin_price,
# 							#p_arr_remain_value
# 							arr_remain_amount,
# 							#p_import_date
# 							up_date,
# 							#p_use_date
# 							start_use_date,
# 							#p_state_id
# 							state_id,
# 							#p_goal_id
# 							goal_id,
# 							#p_country_id
# 							country_id,
# 							#p_supplier_id
# 							supplier_id,
# 							#p_arr_capital_id
# 							arr_capital_id,
# 							#p_amortize_id
# 							method_id,
# 							#p_reason_id
# 							reason_id,
# 							#p_dept_id
# 							dept_id,
# 							#p_staff_id
# 							None,
# 							#p_username
# 							request.user.username,
# 							#p_note
# 							note,
# 							#p_buy_date
# 							buy_date,
# 							#p_amortize_date
# 							atrophy_date,
# 							#p_project_id
# 							project_id,
# 							#p_unit
# 							unit_code,
# 							#p_product_date
# 							product_date,
# 							#p_power
# 							power,
# 							#p_source
# 							source_code,
# 							#p_decision_no
# 							decision_no,
# 							#p_document_status
# 							document_status,
# 							#p_name
# 							asset_name,
# 							#p_interval
# 							interval,
# 							#p_parent_serial
# 							parent_serial,
# 							#p_decision_date
# 							decision_date,
# 							#p_quantity
# 							quantity,
# 							#p_model
# 							model,
# 							#p_product_seri
# 							product_seri
# 						))
# 			cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' "  
#                                        "NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")
# 			cursor.close()
# 			if p_error.getvalue() is not None:
# 				raise Exception(p_error.getvalue())
			context.update({'has_success':_(u"Sửa tài sản thành công")})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("asset/edit-increment-asset.html", context, RequestContext(request))