import json

from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.Dept import Dept


def index(request):
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