# -*- coding: utf-8 -*-
import json

import cx_Oracle
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.db import connection
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, resolve_url
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from myapp.models.Dept import Dept
from myapp.models.List import List
from myapp.models.StockAssetSerial import StockAssetSerial
from myapp.util.DateEncoder import DateEncoder


@login_required(login_url='/login/')
@permission_required('myapp.release_asset',login_url='/permission-error/')
def index(request):
    context = {}
    if request.POST:
        try:
            lsSerial = request.POST["txtListSerial"];
            arrSerial = lsSerial.split(',')
            txtNote = request.POST["txtNote"];
            p_type= '2'
            user_name = request.user.username
            for serial in arrSerial :
                stockAssetSerial =StockAssetSerial.objects.get(serial = serial)
                p_parent_serial = stockAssetSerial.parent_serial
                p_serial = stockAssetSerial.serial
                cursor = connection.cursor()
                cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS' "  
                                           "NLS_TIMESTAMP_FORMAT = 'DD/MM/YYYY HH24:MI:SS.FF'")
                p_error = cursor.var(cx_Oracle.STRING).var
                cursor.callproc("pck_asset.join_release_asset",
                            (
                                # p_error
                                p_error,
                                # p_type
                                p_type,
                                # p_parent_serial
                                p_parent_serial,
                                # p_serial
                                p_serial,
                                # p_note
                                txtNote,
                                # p_user_name
                                user_name,
                            ))
                cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' "  
                                           "NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")
                cursor.close()
                if p_error.getvalue() is not None:
                    raise Exception(p_error.getvalue())
                context.update({'has_success':_(u"Tách tài sản thành công")})
        except Exception as ex:
            context.update({'has_error':str(ex)})
    try:
        context.update({'depts':Dept.objects.all()})
        
        stock_asset_serials_qs = List.objects.raw("""
                        SELECT id,name,serial,parent_serial,connect_by_isleaf is_leaf
                                FROM stock_asset_serial 
                                WHERE (stock_asset_serial.parent_serial is null AND stock_asset_serial.num_sub >0) OR stock_asset_serial.parent_serial is not null
                                START WITH parent_serial IS NULL
                                CONNECT BY PRIOR serial = parent_serial 
                                ORDER SIBLINGS BY parent_serial
                        """)
        stock_asset_serials = []
        for stock_asset_serial in stock_asset_serials_qs:
            row = {}
            row.update({'id':stock_asset_serial.id})
            row.update({'name':stock_asset_serial.name})
            row.update({'serial':stock_asset_serial.serial})
            if stock_asset_serial.parent_serial is not None :
                st =StockAssetSerial.objects.get(serial = stock_asset_serial.parent_serial)
                row.update({'parent_id':st.id})
                row.update({'parent_name':st.name})
                if(stock_asset_serial.is_leaf == 1):
                    row.update({'icon':'/tree/css/zTreeStyle/img/diy/8.png'})
            else:
                row.update({'open':True,'iconOpen':'/tree/css/zTreeStyle/img/diy/1_open.png', 'iconClose':'/tree/css/zTreeStyle/img/diy/1_close.png'})
            stock_asset_serials.append(row)
        context.update({'data':json.dumps(stock_asset_serials,cls=DateEncoder)})
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
    return render_to_response("asset/release-asset.html", context, RequestContext(request))
def getStockAssetSerial(request,stock_id):
    try:
        stock_asset_serials=[]
        stock_asset_serials_qs = List.objects.raw("""
                        SELECT id,name,serial,parent_serial,connect_by_isleaf is_leaf
                                FROM stock_asset_serial 
                                WHERE ((stock_asset_serial.parent_serial is null AND stock_asset_serial.num_sub >0) OR stock_asset_serial.parent_serial is not null) 
                                AND stock_id = """ +"'"+stock_id + "' "+
                                """START WITH parent_serial IS NULL
                                CONNECT BY PRIOR serial = parent_serial 
                                ORDER SIBLINGS BY parent_serial
                        """)
        for stock_asset_serial in stock_asset_serials_qs:
            row = {}
            row.update({'id':stock_asset_serial.id})
            row.update({'name':stock_asset_serial.name})
            row.update({'serial':stock_asset_serial.serial})
            if stock_asset_serial.parent_serial is not None :
                st =StockAssetSerial.objects.get(serial = stock_asset_serial.parent_serial)
                row.update({'parent_id':st.id})
                row.update({'parent_name':st.name})
                if(stock_asset_serial.is_leaf == 1):
                    row.update({'icon':'/tree/css/zTreeStyle/img/diy/8.png'})
            else:
                row.update({'open':True,'iconOpen':'/tree/css/zTreeStyle/img/diy/1_open.png', 'iconClose':'/tree/css/zTreeStyle/img/diy/1_close.png'})
            stock_asset_serials.append(row)
        return HttpResponse(json.dumps({'stock_asset_serials':stock_asset_serials},cls=DateEncoder) ,content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({"error": str(ex)}),content_type="application/json")
