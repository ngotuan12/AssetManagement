'''
Created on Apr 3, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.StockAssetSerial import StockAssetSerial
from django.http.response import HttpResponseRedirect


@login_required(login_url='/login')
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
		context.update({'serial':serial})
		if(request.POST):
			original_amount = request.POST["txtOriginalAmount"]
			serial.original_value = original_amount
			serial.save()
			return HttpResponseRedirect("/verify-asset")
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("asset/verify-asset-edit.html", context,RequestContext(request))