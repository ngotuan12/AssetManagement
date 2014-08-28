'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models import Area, Device


@login_required(login_url='/login')
@permission_required('myapp.view_device',login_url='/permission-error')
def index(request):
	try:
		lsArea = Area.objects.filter(level = '2')
		lsDevice  = Device.objects.all()
		context={'lsArea':lsArea,'lsDevice':lsDevice}
		context.update(csrf(request))
	except Exception as ex:
		context={}
		print(ex)
	finally:
		return render_to_response("device.html", context,RequestContext(request))