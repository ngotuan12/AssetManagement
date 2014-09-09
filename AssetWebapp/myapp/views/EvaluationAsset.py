'''
Created on Apr 3, 2014

@author: TuanNA
'''
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
from myapp.models.StockAssetSerial import StockAssetSerial
from myapp.models.Supplier import Supplier
import cx_Oracle

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
			
			username = request.user.username
			dtEvalution = request.POST["dt_evalution"]
			serial_id = request.POST["slSerial"]
			state_id = request.POST["slState"]
			note = request.POST["txtNote"]
			remain_amount = request.POST["txtRemainAmount"]
			
			stockAssetSerial = StockAssetSerial.objects.get(id=serial_id)
			
			p_serial = stockAssetSerial.serial
# 			p_error =""
			cursor = connection.cursor()
			
			cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'DD/MM/YYYY HH24:MI:SS.FF'")
			p_error = cursor.var(cx_Oracle.STRING).var
			cursor.callproc("pck_asset.update_asset",
						(
							#p_error
							p_error,
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
							username
# 							#p_check_date
# 							dtEvalution
						))
# 			print(p_error.getvalue())
			cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")
			cursor.close()
			if p_error.getvalue() is not None:
				raise Exception(p_error.getvalue())
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("asset/evaluation-asset.html", context, RequestContext(request))
