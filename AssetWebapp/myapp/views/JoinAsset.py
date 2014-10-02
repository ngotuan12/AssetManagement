# -*- coding: utf-8 -*-
import json

import cx_Oracle
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.db import connection
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from myapp.models.Dept import Dept
from myapp.models.List import List
from myapp.models.StockAssetSerial import StockAssetSerial
from myapp.util.DateEncoder import DateEncoder


@login_required(login_url='/login/')
@permission_required('myapp.view_join_asset',login_url='/permission-error/')
def index(request):
    context = {}
    if request.POST:
        try:
            p_type = '1'
            user_name = request.user.username
            
            txtNote = request.POST["txtNote"];
            lsChildSerial = request.POST["hd_ListChildSerial"];
            parentSerial = request.POST["hd_ParentSerial"];
            
            arrChildSerial = lsChildSerial.split(',')
            print("txtNote: "+txtNote)
            print("parentSerial: "+ parentSerial)
            print("lsChildSerial: "+ lsChildSerial)
            for childSerial in arrChildSerial:
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
                                parentSerial,
                                # p_serial
                                childSerial,
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
                context.update({'has_success':_(u"Gộp tài sản thành công")})
        except Exception as ex:
            context.update({'has_error':str(ex)})
    try:
        context.update({'depts':Dept.objects.all()})
        
        child_stock_asset_serials=[]
        parent_stock_asset_serials=[]
        
        getChild(child_stock_asset_serials)
        context.update({'child_data':json.dumps(child_stock_asset_serials,cls=DateEncoder)})
        
        getParent(parent_stock_asset_serials)
        context.update({'parent_data':json.dumps(parent_stock_asset_serials,cls=DateEncoder)})
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
    return render_to_response("asset/_goal_.html", context, RequestContext(request))
def getParent(parent_stock_asset_serials):
    parent_stock_asset_serials_qs = List.objects.raw("""
                        SELECT id,name,serial,parent_serial,connect_by_isleaf is_leaf
                                FROM stock_asset_serial 
                                START WITH parent_serial IS NULL
                                CONNECT BY PRIOR serial = parent_serial 
                                ORDER SIBLINGS BY parent_serial
                        """)
    for stock_asset_serial in parent_stock_asset_serials_qs:
            row = {}
            row.update({'id':stock_asset_serial.id})
            row.update({'name':stock_asset_serial.name})
            row.update({'serial':stock_asset_serial.serial})
            if stock_asset_serial.parent_serial is not None:
                st =StockAssetSerial.objects.get(serial = stock_asset_serial.parent_serial)
                row.update({'parent_id':st.id})
                row.update({'parent_name':st.name})
                row.update({'icon':'/tree/css/zTreeStyle/img/diy/8.png'})
                row.update({'serial':stock_asset_serial.serial})
            else:
                row.update({'open':True,'iconOpen':'/tree/css/zTreeStyle/img/diy/1_open.png', 'iconClose':'/tree/css/zTreeStyle/img/diy/1_close.png'})
            parent_stock_asset_serials.append(row)
def getChild(child_stock_asset_serials):
    child_stock_asset_serials_qs = List.objects.raw("""
                        SELECT id,name,serial
                                FROM stock_asset_serial
                                WHERE parent_serial is null
                                ORDER BY id DESC
                        """)
    for stock_asset_serial in child_stock_asset_serials_qs:
        row = {}
        row.update({'id':stock_asset_serial.id})
        row.update({'name':stock_asset_serial.name})
        row.update({'serial':stock_asset_serial.serial})
        row.update({'icon':'/tree/css/zTreeStyle/img/diy/8.png'})
        child_stock_asset_serials.append(row)
def getListChild(request,stock_id):
    try:
        child_stock_asset_serials_qs = List.objects.raw("""
                            SELECT id,name,serial
                                    FROM stock_asset_serial
                                    WHERE parent_serial is null AND stock_id = '23' 
                                    ORDER BY id DESC
                            """)
        child_stock_asset_serials =[]
        for stock_asset_serial in child_stock_asset_serials_qs:
            row = {}
            row.update({'id':stock_asset_serial.id})
            row.update({'name':stock_asset_serial.name})
            row.update({'serial':stock_asset_serial.serial})
            row.update({'icon':'/tree/css/zTreeStyle/img/diy/8.png'})
            child_stock_asset_serials.append(row)
        return HttpResponse(json.dumps({'child_stock_asset_serials':child_stock_asset_serials},cls=DateEncoder) ,content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({"error": str(ex)}),content_type="application/json")