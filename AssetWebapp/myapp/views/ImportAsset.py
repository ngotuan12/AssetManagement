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

from AssetWebapp.settings import UPLOAD_ROOT
from sc.util.base import handle_uploaded_file
import xlrd
from django.db import connection
from datetime import datetime
import cx_Oracle
from __builtin__ import isinstance
from myapp.util import client


def index(request):
    context={}
    return render_to_response("asset/import-asset.html", context, RequestContext(request))
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
                                    <input id="real-uploaded-file" name="real-uploaded-file" type="hidden" value="%s"/>
                                </form>
                                """
                                % (_(u"Bạn đang chọn file <strong>%s</strong> ")% fileName,uploaded_file,fileName))
        except Exception as ex:
            return HttpResponse(str(ex))
def do_import_temp(request):
    try:
        if request.method == 'POST':
            file_name = request.POST["uploaded-file"]
            real_file_name = request.POST["real-uploaded-file"]
            description = request.POST["description"]
            work_book = xlrd.open_workbook(UPLOAD_ROOT + "/" + file_name)
            sheet= work_book.sheet_by_index(0)
            from_row=5
            to_row = sheet.nrows
            to_columns=25
            cursor = connection.cursor()
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'DD/MM/YYYY HH24:MI:SS.FF'")
            #get file id
            log_error='<br/>'
            p_error = cursor.var(cx_Oracle.STRING).var
            p_file_id = cursor.var(cx_Oracle.NUMBER).var
            cursor.callproc("pck_import.get_file_id",(p_error,
                                                      p_file_id,
                                                      real_file_name,
                                                      description,
                                                      request.user.username
                                                      ))
            if(p_error.getvalue() is None):
                #result_file_name="result"+datetime.now().strftime("%Y%m%d%H%M%S")+".txt"
                #result_path=LOG_ROOT+"/"+result_file_name
                #text_file = open(result_path, "w")
                success=0
                file_id=int(p_file_id.getvalue())
                for i in range(from_row,to_row):
                    p_error = cursor.var(cx_Oracle.STRING).var
                    p_stt=sheet.cell_value(i,0)
                    p_goc=None
                    p_ts_con=None
                    p_ten_ts=sheet.cell_value(i,1)
                    p_ma_da=None
                    p_donvi=sheet.cell_value(i,3)
                    p_stts=sheet.cell_value(i,4)
                    p_ma_nhandien=sheet.cell_value(i,5)
                    p_ma_nguon_von=sheet.cell_value(i,6)
                    p_nuoc_sx=sheet.cell_value(i,7)
                    p_ma_mucdich=sheet.cell_value(i,8)
                    p_soluong=sheet.cell_value(i,9)
                    if(isinstance(p_soluong,str) and p_soluong.strip()==''):
                        p_soluong=None
                    p_nam_sx=sheet.cell_value(i,10)
                    p_cong_suat=sheet.cell_value(i,11)
                    p_thoigian_sd=datetime(*xlrd.xldate_as_tuple(sheet.cell_value(i,12), 0))
                    p_thang_sd=p_thoigian_sd.strftime("%m")
                    p_nam_sd=p_thoigian_sd.strftime("%Y")
                    p_tg_khauhao=sheet.cell_value(i,13)
                    if(isinstance(p_tg_khauhao,str) and p_tg_khauhao.strip()==''):
                        p_tg_khauhao=None
                    p_nguyen_gia=sheet.cell_value(i,14)
                    p_gtcl=sheet.cell_value(i,15)
                    p_dang_sd=sheet.cell_value(i,16)
                    p_khong_sd=sheet.cell_value(i,17)
                    p_ttvt=sheet.cell_value(i,18)
                    p_phongban=sheet.cell_value(i,19)
                    p_nguon_goc=sheet.cell_value(i,20)
                    p_so_qd_pdqt=sheet.cell_value(i,21)
                    p_nam_qd_pdqt=sheet.cell_value(i,22)
                    p_tkht=sheet.cell_value(i,23)
                    p_tinhtrang_hs=sheet.cell_value(i,24)
                    p_ghi_chu=sheet.cell_value(i,25)
                    try:
                        cursor.callproc("pck_import.load_asset_serial",(p_error,
                                                            p_stt,
                                                            p_goc,
                                                            p_ts_con,
                                                            p_ten_ts,
                                                            p_ma_da,
                                                            p_donvi,
                                                            p_stts,
                                                            p_ma_nhandien,
                                                            p_ma_nguon_von,
                                                            p_nuoc_sx,
                                                            p_ma_mucdich,
                                                            p_soluong,
                                                            p_nam_sx,
                                                            p_cong_suat,
                                                            p_thang_sd,
                                                            p_nam_sd,
                                                            p_tg_khauhao,
                                                            p_nguyen_gia,
                                                            p_gtcl,
                                                            p_dang_sd,
                                                            p_khong_sd,
                                                            p_ttvt,
                                                            p_phongban,
                                                            p_nguon_goc,
                                                            p_so_qd_pdqt,
                                                            p_nam_qd_pdqt,
                                                            p_tkht,
                                                            p_tinhtrang_hs,
                                                            p_ghi_chu,
                                                            request.user.username,
                                                            file_id,
                                                            file_name,))
                        if(p_error.getvalue() is None):
                            success=success+1
                            #text_file.write("Dòng %s : %s\n" %(i,'Thành công'))
                        else:
                            #text_file.write("Dòng %s : %s\n" %(i,p_error.getvalue()))
                            log_error=log_error+"Dòng %s : %s <br/>" %(i,p_error.getvalue())
                    except Exception as ex1:
                        #text_file.write("Dòng %s : %s\n" %(i,str(ex1)))
                        log_error=log_error+"Dòng %s : %s <br/>" %(i,str(ex1))
                #text_file.close()
                return HttpResponse(json.dumps({"handle":"success","file_name":real_file_name,"total_record":to_row-from_row,"total_success":success,"total_error":to_row-from_row-success,"log_error":log_error,"file_id":file_id},encoding='utf-8') ,content_type="application/json;charset=utf-8")
            #return HttpResponseRedirect("/log/"+result_file_name)
            else:
                return HttpResponse(json.dumps({"handle":"error", "message":p_error.getvalue()}),content_type="application/json;charset=utf-8")
    except Exception as ex:
        return HttpResponse(json.dumps({"handle":"error", "message": str(ex)}),content_type="application/json;charset=utf-8")
def do_commit(request):
    try:
        if request.method == 'POST':
            file_id = request.POST["file-id"]
            real_file_name = request.POST["real-uploaded-file"]
            cursor = connection.cursor()
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'DD/MM/YYYY HH24:MI:SS.FF'")
            #font_err = xlwt.XFStyle()
            #font_err.font.colour_index = xlwt.Style.colour_map['red']
            #font_success = xlwt.XFStyle()
            #font_success.font.colour_index = xlwt.Style.colour_map['blue']
            #copy file
            p_error = cursor.var(cx_Oracle.STRING).var
            cursor.callproc("pck_import.import_asset_serial",(p_error,file_id))
            log=''
            if(p_error.getvalue() is not None):
                log=p_error.getvalue()
                return HttpResponse(json.dumps({"handle":"error", "message": log}),content_type="application/json;charset=utf-8")
            else:
                log='Commit thành công'
                authorization = client.getAuthorization(request.user.username)
                params_object = {
                                    "p_file_id":file_id,
                                    "p_file_name":real_file_name,
                                }
                fileOut = client.exportReportByJasper(authorization, request.user.username, "ketqua_import_ts", params_object,"EXCEL")
                return HttpResponse(json.dumps({"handle":"success","result":log,"result_file":fileOut},encoding='utf-8') ,content_type="application/json;charset=utf-8")
    except Exception as ex:
        return HttpResponse(json.dumps({"handle":"error", "message": str(ex)}),content_type="application/json;charset=utf-8")
