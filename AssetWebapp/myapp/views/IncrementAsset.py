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
from myapp.models.Reason import Reason
from myapp.models.List import List
from myapp.models.Country import Country
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
		if request.POST: 
			cursor = connection.cursor()
			cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", ['dsad'])
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("increment-asset.html", context,RequestContext(request))