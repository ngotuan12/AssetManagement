'''
Created on Apr 3, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.List import List


@login_required(login_url='/login/')
@permission_required('myapp.view_area', login_url='/permission-erro/r')
def index(request):
	context = {}
	try:
		projects = List.objects.filter(list_type = '7').order_by('create_datetime')
		context.update({'projects':projects})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("category/list-project.html", context, RequestContext(request))
def edit_project(request,project_id):
	print(project_id);
	context = {}
	try:
		projects = List.objects.filter(list_type = '7').order_by('create_datetime')
		context.update({'projects':projects})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
		return render_to_response("category/list-project.html", context, RequestContext(request))