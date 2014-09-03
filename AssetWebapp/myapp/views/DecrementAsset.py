'''
Created on Apr 3, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.Dept import Dept


@login_required(login_url='/login')
@permission_required('myapp.view_decrement_asset',login_url='/permission-error')
def index(request):
	context = {}
	try:
		context.update({'depts':Dept.objects.all()})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("asset/decrement-asset.html", context,RequestContext(request))