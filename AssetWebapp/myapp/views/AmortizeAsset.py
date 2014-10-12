# -*- coding: utf-8 -*-
'''
Created on Sep 9, 2014

@author: vinhndq
'''
from datetime import datetime
import json

import cx_Oracle
from django.contrib.auth.decorators import login_required, permission_required
from django.db import connection
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.AmortizeAsset import AmortizeAsset
from myapp.models.StockAssetSerial import StockAssetSerial


@login_required(login_url='/login/')
@permission_required('myapp.amortize_asset',login_url='/permission-error/')
def index(request):
    try:
        context={}
        sql = '''SELECT a.* from stock_asset_serial a,stock b
                    WHERE a.stock_id=b.stock_id
                        and b.staff_id in (select staff_id from staff where lower(staff_code)=lower(%s)) 
                '''
        assets = StockAssetSerial.objects.raw(sql,[request.user.username])
        context.update({"assets":assets})
        if(request.POST):
            submitForm=request.POST['submitForm']
            if submitForm=='calculate':
                month=request.POST['dtAmortizeMonth']
                dtmonth = datetime.strptime(month, '%m/%Y')
                serial=request.POST['slAssetSerial']
                cursor=connection.cursor()
                p_out_error=cursor.var(cx_Oracle.STRING).var
                p_amount=cursor.var(cx_Oracle.NUMBER).var
                cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS' "  
                                           "NLS_TIMESTAMP_FORMAT = 'DD/MM/YYYY HH24:MI:SS.FF'")
                cursor.callproc("pck_asset.calc_amortize",(p_out_error,p_amount,serial.strip(),dtmonth,request.user.username))
                cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' "  
                                           "NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")
                cursor.close()
                if p_out_error.getvalue() is not None:
                    print p_out_error.getvalue()
                    context.update({"has_error":p_out_error.getvalue()})
                else:
                    amortizeAssets=None
                    if serial.strip()!='':
                        amortizeAssets = AmortizeAsset.objects.filter(month=dtmonth,serial_no=serial).order_by("status")
                    else:
                        amortizeAssets = AmortizeAsset.objects.filter(month=dtmonth)
                    context.update(({"amortize_assets": amortizeAssets}))
                    context.update({"has_success":"Tính khấu hao thành công!"})
            else:
                strChoosen=request.POST['txtChooseAsset']
                list_choosen=strChoosen.split(';')
                cursor=connection.cursor()
                p_error=''
                for child_amotize in list_choosen:
                    infos=child_amotize.split(":")
                    p_serial=infos[0]
                    p_month=infos[1]
                    p_out_error=cursor.var(cx_Oracle.STRING).var
                    p_out_amount=cursor.var(cx_Oracle.NUMBER).var
                    cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS' "  
                                               "NLS_TIMESTAMP_FORMAT = 'DD/MM/YYYY HH24:MI:SS.FF'")
                    cursor.callproc("pck_asset.approve_amortize",(p_out_error,p_out_amount,p_serial.strip(),datetime.strptime(p_month,"%m/%Y"),request.user.username))
                    cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' "  
                                               "NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")
                    if p_out_error.getvalue() is not None:
                        p_error=p_error+p_out_error.getvalue()+"<br/>"
                cursor.close()
                if p_error.strip()!='':
                    context.update({"has_error":p_error})
                context.update({"has_success":"Duyệt thành công!"})
        return render_to_response("asset/amortize-asset.html",context, RequestContext(request))
    except Exception as ex:
        return HttpResponse(json.dumps({"has_error": str(ex)}),content_type="application/json")