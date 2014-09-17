import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.forms.models import model_to_dict
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.Dept import Dept
from myapp.util.DateEncoder import DateEncoder


@login_required(login_url='/login/')
@permission_required('myapp.view_department',login_url='/permission-error/')
def index(request):
	context = {}
	try:
		depts = Dept.objects.raw("SELECT id,dept_name,dept_code,parent_code,parent_id,connect_by_isleaf "
								+ "FROM dept " + "START WITH parent_id IS NULL "
								+ "CONNECT BY PRIOR id = parent_id "
								+ "ORDER SIBLINGS BY dept_name")
		infors =[]
		for dept in depts:
			infors.append(model_to_dict(dept))
# 			try:
# # 				infors.append({'id':dept.id,'pId':dept.parent_id.id,'name':dept.namdee})
# 				if(dept.connect_by_isleaf == 1):
# 					infors.append({'id':dept.id,'pId':dept.parent_id.id,'name':dept.name,'icon':'/tree/css/zTreeStyle/img/diy/8.png'})
# 				else:
# 					infors.append({'id':dept.id,'pId':dept.parent_id.id,'name':dept.name})
# 			except Dept.DoesNotExist:
# 				infors.append({'id':dept.id,'pId':None,'name':dept.name, 'open':True,'iconOpen':'/tree/css/zTreeStyle/img/diy/1_open.png', 'iconClose':'/tree/css/zTreeStyle/img/diy/1_close.png'})
		context.update({'data':json.dumps(infors,cls=DateEncoder)})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
	return render_to_response("department/department.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.add_department',login_url='/permission-error/')
def add(request,parent_id):
	context = {}
	try:
		context.update({'data':''})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
	return render_to_response("department/add-department.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.edit_department',login_url='/permission-error/')
def edit(request,dept_id):
	context = {}
	try:
		dept = Dept.objects.filter(id=dept_id)
		context.update({'dept':dept})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
	return render_to_response("department/edit-department.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.delete_department',login_url='/permission-error/')
def delete(request):
	context = {}
	try:
		depts = Dept.objects.raw("SELECT id,dept_name,dept_code,parent_code,parent_id "
								+ "FROM dept " + "START WITH parent_id IS NULL "
								+ "CONNECT BY PRIOR id = parent_id "
								+ "ORDER SIBLINGS BY dept_name")
		infors =[]
		for dept in depts:
			try:
				infors.append({'id':dept.id,'pId':dept.parent_id.id,'name':dept.name})
			except Dept.DoesNotExist:
				infors.append({'id':dept.id,'pId':None,'name':dept.name})
		context.update({'data':json.dumps(infors)})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
	return render_to_response("department/department.html", context, RequestContext(request))