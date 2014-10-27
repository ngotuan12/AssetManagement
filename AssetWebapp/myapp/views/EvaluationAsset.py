# -*- coding: utf-8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''
import json

import cx_Oracle
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.db import connection
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from myapp.models.Asset import Asset
from myapp.models.Country import Country
from myapp.models.Dept import Dept
from myapp.models.List import List
from myapp.models.Stock import Stock
from myapp.models.StockAssetSerial import StockAssetSerial
from myapp.models.Supplier import Supplier


@login_required(login_url='/login/')
@permission_required('myapp.evaluation_asset', login_url='/permission-error/')
def index(request):
    context = {}
    try:
        assets = Asset.objects.all()
        context.update({'assets':assets, 'methods':List.objects.filter(list_type='6'), 'sources':List.objects.filter(list_type='3')})
        
        reasons_inc = List.objects.raw("""
                                    SELECT id, name, code
                                    FROM list
                                    WHERE CONNECT_BY_ISLEAF = 1 AND list_type = '5'
                                    START WITH parent_id = (SELECT id
                                    FROM list
                                    WHERE code = '10' AND list_type = '5')
                                    CONNECT BY PRIOR id = parent_id
                                    """)
        reasons_dec = List.objects.raw("""
                                    SELECT id, name, code
                                    FROM list
                                    WHERE CONNECT_BY_ISLEAF = 1 AND list_type = '5'
                                    START WITH parent_id = (SELECT id
                                    FROM list
                                    WHERE code = '20' AND list_type = '5')
                                    CONNECT BY PRIOR id = parent_id
                                    """)
        context.update({'reasons_inc':reasons_inc})
        context.update({'reasons_dec':reasons_dec})
        context.update({'countries':Country.objects.all()})
        context.update({'suppliers':Supplier.objects.all()})
        context.update({'depts':Dept.objects.all()})
        context.update({'stocks':Stock.objects.all()})
        context.update({'goals':List.objects.filter(list_type='2')})
        context.update({'states':List.objects.filter(list_type='4')})
        context.update({'capitals':List.objects.filter(list_type='3')})
        if request.POST: 
            # Get parameter
            username = request.user.username
            stock_asset_serial_id = request.POST["hd_stock_asset_serial_id"]
            ls_capital_id = request.POST["hd_ls_capital__id"]
            state_id = request.POST["slState"]
            goal_id = request.POST["slGoal"]
            reason_id = request.POST["slReason"]
            note = request.POST["txtNote"]
            interval = request.POST["txtInterval"]
            arrCapitalId = ls_capital_id.split(';')
            arr_original_value =""
            arr_remain_value =""
            arr_capital_id=str(ls_capital_id)+";"
            stockAssetSerial = StockAssetSerial.objects.get(id=stock_asset_serial_id)
            p_serial = stockAssetSerial.serial
            for c in arrCapitalId :
                capitalId =c
                arr_original_value += str(request.POST["txtAssetOriginal"+capitalId])+ ";"
                arr_remain_value += str(request.POST["txtAssetRemain"+capitalId])+ ";"
            # Get parameter
            p_error =""
            cursor = connection.cursor()
              
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'DD/MM/YYYY HH24:MI:SS.FF'")
            p_error = cursor.var(cx_Oracle.STRING).var
            cursor.callproc("pck_asset.update_asset",
                        (
                            #p_error
                            p_error,
                            #p_serial
                            p_serial,
                            #p_arr_capital
                            arr_capital_id,
                            #p_arr_original_value
                            arr_original_value,
                            #p_arr_remain_amount
                            arr_remain_value,
                            #p_interval
                            interval,
                            #p_state_id
                            state_id,
                            #p_goal_id
                            goal_id,
                            #p_note
                            note,
                            #p_user_name
                            username,
                            #p_reason_id
                            reason_id
                        ))
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")
            cursor.close()
            if p_error.getvalue() is not None:
                raise Exception(p_error.getvalue())
            context.update({'has_success':_(u"Giao dịch thành công")})
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
        return render_to_response("asset/evaluation-asset.html", context, RequestContext(request))
def get_list_stock_serial(request,stock_id):
    try:
        serials_qs = List.objects.raw("""
                                SELECT a.id, a.stock_id, a.asset_id, a.serial, a.original_value,
                                       a.remain_value,a.state_id,b.name as state_name, a.goal_id,c.name as goal_name,a.capital_id,
                                       a.interval, a.source, a.name as name
                              FROM stock_asset_serial a ,list b,list c
                              WHERE a.state_id =b.id AND a.goal_id =c.id AND a.stock_id="""+stock_id+"""
                                """)
        serials = []
        for serial in serials_qs:
            row = {}
            row.update({'id':serial.id})
            row.update({'name':serial.name})
            row.update({'serial':serial.serial})
            row.update({'state_id':serial.state_id})
            row.update({'state_name':serial.state_name})
            row.update({'goal_id':serial.goal_id})
            row.update({'goal_name':serial.goal_name})
            row.update({'interval':serial.interval})
            row.update({'original_value':str(serial.original_value)})
            row.update({'remain_value':str(serial.remain_value)})
            serials.append(row)
        return HttpResponse(json.dumps({'serials':serials,}) ,content_type="application/json")
    except Exception as ex:
        print(ex)
        return HttpResponse(json.dumps({"error": str(ex)}),content_type="application/json")