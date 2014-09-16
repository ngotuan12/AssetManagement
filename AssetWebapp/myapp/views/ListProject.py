'''
Created on Apr 3, 2014

@author: TuanNA
'''
from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
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
	try:
		context = {}
		project = List.objects.get(id = project_id)
		context.update({"project":project}) 
		if request.POST :
			try:
				project_code = request.POST['txtCode']
				project_name = request.POST['txtName']
				project_desciption = request.POST['txtDescription']
				project_createDate = datetime.strptime(request.POST['dt_project'],'%d/%M/%Y')
				
				project.code = project_code
				project.name=project_name
				project.description=project_desciption
				project.create_datetime = project_createDate
				project.save()
				return HttpResponseRedirect("/list-project/")
			except Exception as ex:
				context.update({'has_error':ex})
		context.update(csrf(request))
		return render_to_response("category/edit-project.html",context, RequestContext(request))
	except List.DoesNotExist:
		return HttpResponseRedirect("/notfound-error")
def add_project(request):
	try:
		context = {}
		if request.POST :
			try:
				project_code = request.POST['txtCode']
				project_name = request.POST['txtName']
				project_desciption = request.POST['txtDescription']
				project_createDate = datetime.strptime(request.POST['dt_project'],'%d/%M/%Y')
				
				project = List()
				project.code = project_code
				project.name=project_name
				project.description=project_desciption
				project.create_datetime = project_createDate
				project.list_type = '7'
				project.save()
				return HttpResponseRedirect("/list-project/")
			except Exception as ex:
				context.update({'has_error':ex})
		context.update(csrf(request))
		return render_to_response("category/add-project.html",context, RequestContext(request))
	except List.DoesNotExist:
		return HttpResponseRedirect("/notfound-error")
@login_required(login_url='/login/')
def delete_reason(request,project_id):
	try:
		if request.POST:
			project = List.objects.get(id=project_id)
			project.delete()
		return HttpResponseRedirect("/list-project/")
	except List.DoesNotExist:
			return HttpResponseRedirect("/notfound-error")