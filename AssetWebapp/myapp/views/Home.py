'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models import Device


@login_required(login_url='/login')
def index(request):
	devices = Device.objects.all()
	context={'devices':devices}
	return render_to_response("index.html", context, RequestContext(request))