# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.List import List
from myapp.util.DateEncoder import DateEncoder
from django.http.response import HttpResponseRedirect


@login_required(login_url='/login/')
@permission_required('myapp.view_department',login_url='/permission-error/')
def index(request):
    context = {}
    try:
        volatilities_qs = List.objects.raw("""
                                SELECT id,name,code,description,list_level,status,list_type,
                                    create_datetime,user_name,parent_id,connect_by_isleaf is_leaf
                                FROM list 
                                WHERE list_type='5' 
                                START WITH parent_id IS NULL 
                                CONNECT BY PRIOR id = parent_id 
                                ORDER SIBLINGS BY parent_id 
                                """)
        volatilities = []
        for volatility in volatilities_qs:
            row = {}
            row.update({'id':volatility.id})
            row.update({'code':volatility.code})
            row.update({'name':volatility.name})
            row.update({'description':volatility.description})
            row.update({'list_level':volatility.list_level})
            row.update({'status':volatility.status})
            row.update({'create_date':volatility.create_datetime.strftime('%Y-%m-%d %H:%M:%S')})
            row.update({'user_name':volatility.user_name})
            try:
                row.update({'parent_id':volatility.parent_id.id})
                row.update({'parent_name':volatility.parent_id.name})
                if(volatility.is_leaf == 1):
                    row.update({'icon':'/tree/css/zTreeStyle/img/diy/8.png'})
            except:
                row.update({'open':True,'iconOpen':'/tree/css/zTreeStyle/img/diy/1_open.png', 'iconClose':'/tree/css/zTreeStyle/img/diy/1_close.png'})
            volatilities.append(row)
        context.update({'data':json.dumps(volatilities,cls=DateEncoder)})
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
    return render_to_response("asset/asset-volatility.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.add_department',login_url='/permission-error/')
def add(request,parent_id):
    context = {}
    try:
        parent = List.objects.get(id=parent_id,list_type='5')
        context.update({'parent_name':parent.name})
        if request.POST:
            code = request.POST["txtCode"]
            name = request.POST["txtName"]
            description = request.POST["txtDescription"]
            
            asset_volatility = List()
            asset_volatility.code = code
            asset_volatility.name = name
            asset_volatility.description = description
            asset_volatility.list_type = '5'
            if request.POST.get('ckStatus'):
                asset_volatility.status = "1"
            else:
                asset_volatility.status = "0"
            asset_volatility.parent_id = parent
            asset_volatility.user_name = request.user.username
            check_asset_volatility = List.objects.filter(code = code,parent_id = parent_id,list_type='5')
            if len(check_asset_volatility) > 0:
                context.update({'has_error':'Mã biến động tài sản đã tồn tại'})
                context.update({'asset_volatility':asset_volatility})
            else:
                asset_volatility.save()
                return HttpResponseRedirect("/asset-volatility/")
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
    return render_to_response("asset/add-asset-volatility.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.edit_department',login_url='/permission-error/')
def edit(request,volatility_id):
    context = {}
    try:
        asset_volatility = List.objects.get(id=volatility_id,list_type='5')
        context.update({'parents':List.objects.exclude(id=volatility_id).filter(list_type='5')})
        context.update({'asset_volatility':asset_volatility})
        if request.POST:
            parent_id = request.POST["slParent"]
            code = request.POST["txtCode"]
            name = request.POST["txtName"]
            description = request.POST["txtDescription"]
            #update
            asset_volatility.code = code
            asset_volatility.name = name
            asset_volatility.description = description
            if request.POST.get('ckStatus'):
                asset_volatility.status = "1"
            else:
                asset_volatility.status = "0"
            asset_volatility.parent_id = List.objects.get(id=parent_id,list_type='5')
            check_asset_volatility = List.objects.exclude(id=volatility_id).filter(code = code,parent_id = parent_id,list_type='5')
            if len(check_asset_volatility) >0 :
                context.update({'has_error':'Mã biến động tài sản đã tồn tại'})
            else:
                asset_volatility.save()
                return HttpResponseRedirect("/asset-volatility/")
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
    return render_to_response("asset/edit-asset-volatility.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.delete_department',login_url='/permission-error/')
def delete(request,volatility_id):
    context = {}
    try:
        if request.POST:
            asset_volatility = List.objects.get(id=volatility_id,list_type='5')
            asset_volatility.delete()
            return HttpResponseRedirect("/asset-volatility/")
    except Exception as ex:
        context.update({'has_error':str(ex)})
        return HttpResponseRedirect("/asset-state/")
