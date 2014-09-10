# -*- coding: utf-8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''
import cx_Oracle
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.db import connection
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.Asset import Asset
from myapp.models.Country import Country
from myapp.models.Dept import Dept
from myapp.models.List import List
from myapp.models.Reason import Reason
from myapp.models.Stock import Stock
from myapp.models.StockAssetSerial import StockAssetSerial
from myapp.models.Supplier import Supplier
from myapp.models.Staff import Staff

@login_required(login_url='/login/')
@permission_required('myapp.view_area', login_url='/permission-error/')
def index(request):
    context = {}
    try:
        assets = Asset.objects.all()
        context.update({'assets':assets, 'reasons':Reason.objects.filter(group_code='3'), 'methods':List.objects.filter(list_type='6'), 'sources':List.objects.filter(list_type='3')})
        
        context.update({'countries':Country.objects.all()})
        context.update({'suppliers':Supplier.objects.all()})
        context.update({'depts':Dept.objects.all()})
        context.update({'stocks':Stock.objects.all()})
        context.update({'goals':List.objects.filter(list_type='2')})
        context.update({'states':List.objects.filter(list_type='4')})
        context.update({'staffs':Staff.objects.all()})
        if request.POST: 
            # Get parameter
            
            serial_source_id = request.POST["slSerialSource"]
            username = request.user.username
            stock_des_id = request.POST["slStockDes"]
            reason_id = request.POST["slReason"]
            note = request.POST["txtNote"]
            
            stockAssetSerial = StockAssetSerial.objects.get(id=serial_source_id)
            
            stock_source_id = stockAssetSerial.stock.id
            asset_source_id = stockAssetSerial.asset.id
            dept_source_id = stockAssetSerial.stock.dept.id
            p_serial = stockAssetSerial.serial
            
            dtTransfer = request.POST["dt_transfer"]
            staff_id =request.POST["slStaff"]
            
            cursor = connection.cursor()
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'DD/MM/YYYY HH24:MI:SS.FF'")
            p_error = cursor.var(cx_Oracle.STRING).var
            cursor.callproc("pck_stock_trans.change_stock_asset_serial",
                        (
                            #p_error
                            p_error,
                            #p_stock_id
                            stock_source_id,
                            #p_ie_stock_id
                            stock_des_id,
                            #p_asset_id
                            asset_source_id,
                            #p_serial
                            p_serial,
                            #p_date
                            dtTransfer,
                            #p_reason_id
                            reason_id,
#                             #p_dept_id
                            dept_source_id,
                            #p_staff_id
                            staff_id,
                            #p_username
                            username,
                            #p_note
                            note
                        ))
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")
            cursor.close()
            if p_error.getvalue() is not None:
                raise Exception(p_error.getvalue())
            context.update({'has_success':"Chuyển đổi thành công"})
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
        return render_to_response("asset/transfer-asset.html", context, RequestContext(request))