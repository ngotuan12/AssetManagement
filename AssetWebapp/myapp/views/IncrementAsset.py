'''
Created on Apr 3, 2014

@author: TuanNA
'''
import cx_Oracle
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.db import connection
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.Asset import Asset
from myapp.models.Country import Country
from myapp.models.Dept import Dept
from myapp.models.List import List
from myapp.models.Reason import Reason
from myapp.models.Stock import Stock
from myapp.models.Supplier import Supplier


@login_required(login_url='/login/')
@permission_required('myapp.view_area', login_url='/permission-error/')
def index(request):
	context = {}
	try:
		assets = Asset.objects.all()
		context.update({'assets':assets, 'reasons':Reason.objects.filter(group_code='1'), 'methods':List.objects.filter(list_type='6'), 'sources':List.objects.filter(list_type='3')})
		
		context.update({'countries':Country.objects.all()})
		context.update({'suppliers':Supplier.objects.all()})
		context.update({'depts':Dept.objects.all()})
		context.update({'stocks':Stock.objects.all()})
		context.update({'goals':List.objects.filter(list_type='2')})
		context.update({'states':List.objects.filter(list_type='4')})
		if request.POST: 
			# Get parameter
			asset_id = request.POST["slAsset"]
			reason_id = request.POST["slReason"]
			method_id = request.POST["slMethod"]
			source_id = request.POST["slSource"]
			country_id = request.POST["slCountry"]
			supplier_id = request.POST["slSupplier"]
			dept_id = request.POST["slDept"]
			stock_id = request.POST["slStock"]
			goal_id = request.POST["slGoal"]
			state_id = request.POST["slState"]
			buy_date = request.POST["dtBuyDate"]
			start_use_date = request.POST["dtStartUseDate"]
			up_date = request.POST["dtUpDate"]
			atrophy_date = request.POST["dtAtrophyDate"]
			origin_price = request.POST["txtOriginPrice"]
			serial = request.POST["txtSerial"]
			remain_amount = request.POST["txtRemainAmount"]
			note = request.POST["txtNote"]
			p_error  = ''
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
							#p_original_value
							origin_price,
							#p_remain_value
							remain_amount,
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
							#p_capital_id
							source_id,
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
							atrophy_date								
						))
			cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")
			cursor.close()
			if p_error.getvalue() is not None:
				raise Exception(p_error.getvalue())
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("asset/increment-asset.html", context, RequestContext(request))
