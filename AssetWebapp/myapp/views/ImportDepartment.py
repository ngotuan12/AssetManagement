# -*- coding: utf-8 -*-
'''
Created on Oct 22, 2014

@author: TuanNA
'''
import json
import os

from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from AssetWebapp.settings import UPLOAD_ROOT, LOG_ROOT
from sc.util.base import handle_uploaded_file
import xlrd
from django.db import connection
import xlwt
from datetime import datetime
import cx_Oracle


def index(request):
    context={}
    return render_to_response("department/import-department.html", context, RequestContext(request))
def upload(request):
    if request.method == 'POST':
        try:
            fileName,fileExtension = os.path.splitext(request.FILES['file-input'].name)
            if not fileExtension==".xls":
                raise Exception(_(u"Định dạng file phải là excel!"))
            uploaded_file = handle_uploaded_file(request.FILES['file-input'])
            return HttpResponse("""
                                <form id='form-uploaded'> <p style="color: #636e7b;"> %s </p> 
                                    <input id="uploaded-file" name="uploaded-file" type="hidden" value="%s"/>
                                </form>
                                """
                                % (_(u"Bạn đang chọn file <strong>%s</strong> ")% fileName,uploaded_file))
        except Exception as ex:
            return HttpResponse(str(ex))
def do_import(request):
    try:
        if request.method == 'POST':
            file_name = request.POST["uploaded-file"]
            work_book = xlrd.open_workbook(UPLOAD_ROOT + "/" + file_name)
            sheet= work_book.sheet_by_index(0)
            from_row=1
            to_row = sheet.nrows
            to_columns=6
            cursor = connection.cursor()
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'DD/MM/YYYY HH24:MI:SS.FF'")
            result_book=xlwt.Workbook(encoding='utf-8')
            result_sheet=result_book.add_sheet("Result")
            result_file_name="result"+datetime.now().strftime("%Y%m%d%H%M%S")+".xls"
            result_path=LOG_ROOT+"/"+result_file_name
            font_err = xlwt.XFStyle()
            font_err.font.colour_index = xlwt.Style.colour_map['red']
            font_success = xlwt.XFStyle()
            font_success.font.colour_index = xlwt.Style.colour_map['blue']
            #copy file
            success=0
            for i in range(0,to_row):
                p_error = cursor.var(cx_Oracle.STRING).var
                values=[]
                values.append(p_error)
                for j in range(0,to_columns+1):
                    cell_value=sheet.cell_value(i,j)
                    values.append(cell_value)
                    result_sheet.write(i,j,cell_value)
                if i>=from_row:
                    values.append(request.user.username)
                    try:
                        cursor.callproc("pck_import.department",values)
                        if(p_error.getvalue() is not None):
                            result_sheet.write(i,to_columns+1,p_error.getvalue(),font_err)
                        else:
                            success=success+1
                            result_sheet.write(i,to_columns+1,"Thành công",font_success)
                    except Exception as ex1:
                        result_sheet.write(i,to_columns+1,str(ex1),font_err)
                elif i==from_row-1:
                    result_sheet.write(i,to_columns+1,"Kết quả")
            result_book.save(result_path)
            return HttpResponse(json.dumps({"handle":"success","file_name":file_name,"total_record":to_row-1,"total_success":success,"total_error":to_row-1-success,"result_file":result_file_name},encoding='utf-8') ,content_type="application/json;charset=utf-8")
            #return HttpResponseRedirect("/log/"+result_file_name)
    except Exception as ex:
        return HttpResponse(json.dumps({"handle":"error", "message": str(ex)}),content_type="application/json;charset=utf-8")
    