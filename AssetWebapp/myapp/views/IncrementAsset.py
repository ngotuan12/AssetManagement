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
from myapp.models.Supplier import Supplier


@login_required(login_url='/login')
@permission_required('myapp.view_area',login_url='/permission-error')
def index(request):
	context={}
	try:
		assets = Asset.objects.all()
		context.update({'assets':assets,'reasons':Reason.objects.all(),'methods':List.objects.filter(list_type='6'),'sources':List.objects.filter(list_type='3')})
		context.update({'countries':Country.objects.all()})
		context.update({'suppliers':Supplier.objects.all()})
		context.update({'depts':Dept.objects.all()})
		context.update({'stocks':Stock.objects.all()})
		if request.POST: 
			#Get parameter
			asset_id = request.POST["slAsset"]
			reason_id = request.POST["slReason"]
			method_id = request.POST["slMethod"]
			source_id = request.POST["slSource"]
			country_id = request.POST["slCountry"]
			supplier_id = request.POST["slSupplier"]
			dept_id = request.POST["slDept"]
			stock_id = request.POST["slStock"]
			buy_date = request.POST["slStock"]
			start_use_date = request.POST["slStock"]
			up_date = request.POST["slStock"]
			atrophy_date = request.POST["slStock"]
			origin_price = request.POST["txtOriginPrice"]
			remain_amount = request.POST["txtRemainAmount"]
			note = request.POST["txtNote"]
			cursor = connection.cursor()
# 			cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", ['dsad'])
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("asset/increment-asset.html", context,RequestContext(request))