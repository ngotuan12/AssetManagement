'''
Created on Sep 9, 2014

@author: vinhndq
'''
from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import HttpResponse
import json
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db import connection
import cx_Oracle
from datetime import datetime
@login_required(login_url='/login/')
@permission_required('myapp.view_amortize_asset',login_url='/permission-error/')
def index(request):
    try:
        context={}
        if(request.POST):
            month=request.POST['dtAmortizeMonth']
            dMonth=datetime.strptime(month,'%dd/%mm/%yyyy')
            serial=request.POST['txtSerial']
            cursor=connection.cursor()
            p_error=''
            p_amount=cursor.var(cx_Oracle.NUMBER)
            cursor.callproc("pck_asset.calc_amortize",(p_error,p_amount,serial.strip(),dMonth,request.user.username))
            cursor.close()
            if p_error.strip()!='':
                context.update({"has_error":p_error})
        return render_to_response("asset/amortize-asset.html",context, RequestContext(request))
    except Exception as ex:
        return HttpResponse(json.dumps({"has_error": str(ex)}),content_type="application/json")