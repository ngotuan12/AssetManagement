'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models import DeviceProperties


@login_required(login_url='/login')
@permission_required('myapp.view_deviceproperties',login_url='/permission-error')
def index(request):
	lsDeviceProperty = DeviceProperties.objects.all()
	context={'lsDeviceProperty':lsDeviceProperty}
	context.update(csrf(request))
	return render_to_response("device-property.html", context,RequestContext(request))
