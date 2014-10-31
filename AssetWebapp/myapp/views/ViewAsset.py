'''
Created on Apr 3, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
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
from myapp.models.CapitalValue import CapitalValue

@login_required(login_url='/login/')
@permission_required('myapp.view_asset', login_url='/permission-erro/r')
def index(request):
	context = {}
	try:
		assets = Asset.objects.all()
		stockAsset = StockAssetSerial.objects.filter(asset__in=assets)
		reasons =Reason.objects.all()
		methods = List.objects.filter(list_type='6')
		sources = List.objects.filter(list_type='3')
		countries = Country.objects.all()
		suppliers = Supplier.objects.all()
		depts = Dept.objects.all()
		stocks = Stock.objects.all()
		goals = List.objects.filter(list_type='2')
		states = List.objects.filter(list_type='4')
		context.update({'assets':assets,'reasons':reasons, 'methods':methods, 'sources':sources,'states':states,'countries':countries,'suppliers':suppliers,'depts':depts,'stocks':stocks,'goals':goals})
		if request.POST:
			asset_id = request.POST["slAsset"]
			country_id = request.POST["slCountry"]
			stock_id = request.POST["slStock"]
			goal_id = request.POST["slGoal"]
			state_id = request.POST["slState"]
			original = '-1'
			
			stockAsset = StockAssetSerial.objects.all().order_by('-import_date')
			if asset_id !='-1':
				stockAsset = stockAsset.filter(asset =asset_id)
			if stock_id !='-1' :
				stockAsset = stockAsset.filter(stock = stock_id)
			if state_id !='-1':
				stockAsset = stockAsset.filter(state = state_id)
			if goal_id !='-1':
				stockAsset = stockAsset.filter(goal = goal_id)
			if country_id !='-1':
				stockAsset = stockAsset.filter(country = country_id)
			if request.POST["txtOriginal"] :
				original = float(request.POST["txtOriginal"])
				stockAsset = stockAsset.filter(original_value = original)
				lsCapital_value_child =CapitalValue.objects.filter(stock_asset_serial__in =stockAsset)
			context.update({'stockeAssets':lsCapital_value_child})
			context.update({'original':original,'stock_id':stock_id,'country_id':country_id,'asset_id':asset_id,'goal_id':goal_id,'state_id':state_id})
		else :
			asset_id = '-1'
			country_id = '-1'
			stock_id = '-1'
			goal_id = '-1'
			state_id = '-1'
			original = '-1'
			
			stockAsset = StockAssetSerial.objects.all().order_by('-import_date')
			lsCapital_value_child =CapitalValue.objects.filter(stock_asset_serial__in =stockAsset)
			context.update({'stockeAssets':lsCapital_value_child})
			context.update({'original':original,'stock_id':stock_id,'country_id':country_id,'asset_id':asset_id,'goal_id':goal_id,'state_id':state_id})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("asset/view-asset.html", context, RequestContext(request))