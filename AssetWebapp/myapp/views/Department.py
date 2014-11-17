# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.importer.DepartmentImporter import DepartmentImporter
from myapp.models.Dept import Dept
from myapp.util.DateEncoder import DateEncoder
import xlrd
from django.db import connection
import cx_Oracle
import xlwt
from datetime import datetime


@login_required(login_url='/login/')
@permission_required('myapp.view_department', login_url='/permission-error/')
def index(request):
	context = {}
	try:
		depts_qs = Dept.objects.raw("""
								SELECT id,dept_name,dept_code,dept_status,parent_code,
									address,tel,fax,create_datetime,user_name,
									parent_id,connect_by_isleaf is_leaf 
								FROM dept 
								START WITH parent_id IS NULL 
								CONNECT BY PRIOR id = parent_id 
								ORDER SIBLINGS BY dept_name 
								""")
# 		infors = [ {"code":dept.code,"name":dept.name} for dept in depts_qs ]
# 		depts = [dict((dept.code,dept.name)) for dept in depts_qs]
		depts = []
		for dept in depts_qs:
			row = {}
			row.update({'id':dept.id})
			row.update({'code':dept.code})
			row.update({'name':dept.name})
			row.update({'address':dept.address})
			row.update({'tel':dept.tel})
			row.update({'fax':dept.fax})
			row.update({'status':dept.status})
			row.update({'create_date':dept.create_datetime.strftime('%Y-%m-%d %H:%M:%S')})
			row.update({'user_name':dept.user_name})
			try:
				row.update({'parent_id':dept.parent_id.id})
				row.update({'parent_name':dept.parent_id.name})
				if(dept.is_leaf == 1):
					row.update({'icon':'/tree/css/zTreeStyle/img/diy/8.png'})
			except Dept.DoesNotExist:
				row.update({'open':True, 'iconOpen':'/tree/css/zTreeStyle/img/diy/1_open.png', 'iconClose':'/tree/css/zTreeStyle/img/diy/1_close.png'})
			depts.append(row)
		context.update({'data':json.dumps(depts, cls=DateEncoder)})
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
	return render_to_response("department/department.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.add_department', login_url='/permission-error/')
def add(request, parent_id):
	context = {}
	try:
		parent = Dept.objects.get(id=parent_id)
		context.update({'parent_name':parent.name})
		if request.POST:
			code = request.POST["txtCode"]
			name = request.POST["txtName"]
			address = request.POST["txtAddress"]
			tel = request.POST["txtTel"]
			fax = request.POST["txtFax"]
			dept = Dept()
			dept.code = code
			dept.name = name
			dept.address = address
			dept.tel = tel
			dept.fax = fax
			if request.POST.get('ckStatus'):
				dept.status = "1"
			else:
				dept.status = "0"
			dept.parent_id = parent
			dept.user_name = request.user.username
			dept.save()
			return HttpResponseRedirect("/department/")
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
	return render_to_response("department/add-department.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.edit_department', login_url='/permission-error/')
def edit(request, dept_id):
	context = {}
	try:
		dept = Dept.objects.get(id=dept_id)
		context.update({'parents':Dept.objects.exclude(id=dept_id)})
		context.update({'dept':dept})
		if request.POST:
			parent_id = request.POST["slParent"]
			code = request.POST["txtCode"]
			name = request.POST["txtName"]
			address = request.POST["txtAddress"]
			tel = request.POST["txtTel"]
			fax = request.POST["txtFax"]
			# update
			dept.code = code
			dept.name = name
			dept.address = address
			dept.tel = tel
			dept.fax = fax
			if request.POST.get('ckStatus'):
				dept.status = "1"
			else:
				dept.status = "0"
			dept.parent_id = Dept.objects.get(id=parent_id)
			dept.save()
			return HttpResponseRedirect("/department/")
	except Exception as ex:
		context.update({'has_error':str(ex)})
	finally:
		context.update(csrf(request))
	return render_to_response("department/edit-department.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.delete_department', login_url='/permission-error/')
def delete(request, dept_id):
	context = {}
	try:
		if request.POST:
			dept = Dept.objects.get(id=dept_id)
			dept.delete()
			return HttpResponseRedirect("/department/")
	except Exception as ex:
		context.update({'has_error':str(ex)})
		return HttpResponseRedirect("/department/")
def import_from_excel(request):
	context={}
	try:
		if(request.POST):
			input_excel=request.FILES["file-input"]
			work_book = xlrd.open_workbook(file_contents=input_excel.read())
			sheet= work_book.sheet_by_index(0)
			to_row = sheet.nrows
			to_columns=6
			cursor = connection.cursor()
			cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'DD/MM/YYYY HH24:MI:SS.FF'")
			result_book=xlwt.Workbook(encoding='utf-8')
			result_sheet=result_book.add_sheet("Result")
			result_path="C:/Users/vinhndq/Desktop/result"+datetime.now().strftime("%Y%m%d%H%M%S")+".xls"
			font_err = xlwt.XFStyle()
			font_err.font.colour_index = xlwt.Style.colour_map['red']
			font_success = xlwt.XFStyle()
			font_success.font.colour_index = xlwt.Style.colour_map['blue']
			#copy file
			for i in range(0,to_row):
				p_error = cursor.var(cx_Oracle.STRING).var
				values=[]
				values.append(p_error)
				for j in range(0,to_columns):
					cell_value=sheet.cell_value(i,j)
					values.append(cell_value)
					result_sheet.write(i,j,cell_value)
				if i!=0:
					values.append(request.user.username)
					try:
						cursor.callproc("pck_import.department",values)
						if(p_error.getvalue() is not None):
							result_sheet.write(i,to_columns+1,p_error.getvalue(),font_err)
						else:
							result_sheet.write(i,to_columns+1,"Thành công",font_success)
					except Exception as ex1:
						result_sheet.write(i,to_columns+1,str(ex1),font_err)
				else:
					result_sheet.write(i,to_columns+1,"Kết quả")
			result_book.save(result_path)
			return HttpResponseRedirect(result_path)
		return render_to_response("department/import-department.html", context, RequestContext(request))
	except Exception as ex:
		context.update({"has_error":str(ex)})
		return HttpResponseRedirect("/department/import/")
