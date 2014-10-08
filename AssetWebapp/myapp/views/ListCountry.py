# -*- coding: utf-8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''

from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.Country import Country

@login_required(login_url='/login/')
@permission_required('myapp.view-country', login_url='/permission-error/')
def index(request):
	context = {}
	try:
		countries = Country.objects.all().order_by('create_datetime')
		context.update({'countries':countries})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("country/list-country.html", context, RequestContext(request))
