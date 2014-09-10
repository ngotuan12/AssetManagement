# -*- coding: utf-8 -*-
'''
Created on Sep 8, 2014

@author: vinhndq
'''
import json

import cx_Oracle
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.db import connection
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.util.DateEncoder import DateEncoder


@login_required(login_url='/login/')
@permission_required('myapp.release_asset', login_url='/permission-error/')
def release_asset(request):
    try:
        context={}
        #assets=Asset.objects.filter().query("SELECT a.* FROM ASSET a,(select distinct parent_id from ASSET) b where a.id=b.parent_id")
        sql="SELECT a.id,a.code,a.name,b.serial from asset a,stock_asset_serial b where a.id=b.asset_id"
        #assets=Asset.objects.all()
        context.update({"assets":sqltodict(sql, None)})
        if request.POST:
            parent_serial=request.POST['slAsset']
            strChoosen=request.POST['txtChooseAsset']
            note=request.POST['txtNote']
            list_choosen=strChoosen.split(';');
            p_error=''
            for child_asset_serial in list_choosen:
                p_error=p_error + do_join_release_asset("2", parent_serial, child_asset_serial, note, request.user.username)
                if p_error.strip()!='':
                    p_error=p_error+"<br/>"
            if p_error.strip()!='':
                context.update({"has_error":p_error})
            context.update({"has_success":"Tách tài sản thành công!"})
            sql="SELECT a.id,a.code,a.name,b.serial from asset a,stock_asset_serial b where a.id=b.asset_id and b.parent_serial=%s"
            context.update({"child_assets":sqltodict(sql, [parent_serial])})
            context.update({"parent_serial":parent_serial})
        context.update(csrf(request))
        return render_to_response("asset/release-asset.html",context, RequestContext(request))
    except Exception as ex:
        return HttpResponse(json.dumps({"has_error": str(ex)}),content_type="application/json")
@login_required(login_url='/login/')
@permission_required('myapp.join_asset', login_url='/permission-error/')
def join_asset(request):
    try:
        context={}
        sql="SELECT a.id,a.code,a.name,b.serial from asset a,stock_asset_serial b where a.id=b.asset_id and b.parent_serial is null"
        child_assets=sqltodict(sql, None)
        sql="SELECT a.id,a.code,a.name,b.serial from asset a,stock_asset_serial b where a.id=b.asset_id"
        assets=sqltodict(sql, None)
        context.update({"assets":assets})
        context.update({"child_assets":child_assets})
        if request.POST:
            parent_id=request.POST['slAsset']
            strChoosen=request.POST['txtChooseAsset']
            note=request.POST['txtNote']
            list_choosen=strChoosen.split(';');
            p_error=''
            for child_asset in list_choosen:
                p_error=p_error + do_join_release_asset("1", parent_id, child_asset, note, request.user.username)
                if p_error.strip()!='':
                    p_error=p_error+"<br/>"
            if p_error.strip()!='':
                context.update({"has_error":p_error})
            context.update({"has_success":"Gộp tài sản thành công!"})
        context.update(csrf(request))
        return render_to_response("asset/join-asset.html",context, RequestContext(request))
    except Exception as ex:
        return HttpResponse(json.dumps({"has_error": str(ex)}),content_type="application/json")
@login_required(login_url='/login/')
def load_child_asset(request,asset_parent_id):
    try:
        sql="SELECT a.id,a.code,a.name,b.serial from asset a,stock_asset_serial b where a.id=b.asset_id and b.parent_serial=%s"
        infors=sqltodict(sql, [asset_parent_id])
        print infors
        return HttpResponse(json.dumps({'child_assets':infors},cls=DateEncoder) ,content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({"error": str(ex)}),content_type="application/json")
def do_join_release_asset(p_type,p_parent_serial,p_child_serial,p_note,p_user):
    
    try:
        cursor = connection.cursor()
        p_error=cursor.var(cx_Oracle.STRING).var
        cursor.callproc("pck_asset.join_release_asset",
                    (
                        #p_error
                        p_error,
                        #p_type
                        p_type,
                        #p_parent_serial
                        p_parent_serial,
                        #p_serial
                        p_child_serial,
                        #p_note
                        p_note,
                        #p_user
                        p_user,
                    ))
        cursor.close()
        strError =p_error.getvalue() 
        if(strError is None): 
            strError=''
        return strError
    except Exception as ex:
        return str(ex)
    
def sqltodict(query,param):
    cursor = connection.cursor()
    cursor.execute(query,param)
    fieldnames = [name[0] for name in cursor.description]
    result = []
    for row in cursor.fetchall():
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result