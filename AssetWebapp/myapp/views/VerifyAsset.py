'''
Created on Apr 3, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.context import RequestContext

@login_required(login_url='/login')
@permission_required('myapp.view_decrement_asset',login_url='/permission-error')
def index(request):
	context = {}
	try:
		context.update(csrf(request))
	except Exception as ex:
		context={}
		print(ex)
	finally:
		return render_to_response("verify-asset.html", context,RequestContext(request))