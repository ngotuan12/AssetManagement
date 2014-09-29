# -*- coding: utf-8 -*-

import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response, resolve_url
from django.template.context import RequestContext

from myapp.models.List import List
from myapp.util.DateEncoder import DateEncoder


@login_required(login_url='/login/')
@permission_required('myapp.view_department',login_url='/permission-error/')
def index(request):
    context = {}
    try:
        states_qs = List.objects.raw("""
                                SELECT id,name,code,description,list_level,status,list_type,
                                    create_datetime,user_name,parent_id,connect_by_isleaf is_leaf
                                FROM list 
                                WHERE list_type='4' 
                                START WITH parent_id IS NULL 
                                CONNECT BY PRIOR id = parent_id 
                                ORDER SIBLINGS BY parent_id 
                                """)
        states = []
        for state in states_qs:
            row = {}
            row.update({'id':state.id})
            row.update({'code':state.code})
            row.update({'name':state.name})
            row.update({'description':state.description})
            row.update({'list_level':state.list_level})
            row.update({'status':state.status})
            row.update({'create_date':state.create_datetime.strftime('%Y-%m-%d %H:%M:%S')})
            row.update({'user_name':state.user_name})
            try:
                row.update({'parent_id':state.parent_id.id})
                row.update({'parent_name':state.parent_id.name})
                if(state.is_leaf == 1):
                    row.update({'icon':'/tree/css/zTreeStyle/img/diy/8.png'})
            except:
                row.update({'open':True,'iconOpen':'/tree/css/zTreeStyle/img/diy/1_open.png', 'iconClose':'/tree/css/zTreeStyle/img/diy/1_close.png'})
            states.append(row)
        context.update({'data':json.dumps(states,cls=DateEncoder)})
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
    return render_to_response("asset/asset-state.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.add_department',login_url='/permission-error/')
def add(request,parent_id):
    context = {}
    try:
        parent = List.objects.get(id=parent_id,list_type='4')
        context.update({'parent_name':parent.name})
        if request.POST:
            code = request.POST["txtCode"]
            name = request.POST["txtName"]
            description = request.POST["txtDescription"]
            asset_state = List()
            asset_state.code = code
            asset_state.name = name
            asset_state.description = description
            asset_state.list_type = '4'
            if request.POST.get('ckStatus'):
                asset_state.status = "1"
            else:
                asset_state.status = "0"
            asset_state.parent_id = parent
            asset_state.user_name = request.user.username
            check_asset_state = List.objects.filter(code = code,parent_id = parent_id,list_type='4')
            if len(check_asset_state) > 0:
                context.update({'has_error':'Mã hiện trạng tài sản đã tồn tại'})
                context.update({'asset_state':asset_state})
            else:
                asset_state.save()
                return HttpResponseRedirect(resolve_url("asset-state"))
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
    return render_to_response("asset/add-asset-state.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.edit_department',login_url='/permission-error/')
def edit(request,state_id):
    context = {}
    try:
        asset_state = List.objects.get(id=state_id,list_type='4')
        context.update({'parents':List.objects.exclude(id=state_id).filter(list_type='4')})
        context.update({'asset_state':asset_state})
        if request.POST:
            parent_id = request.POST["slParent"]
            code = request.POST["txtCode"]
            name = request.POST["txtName"]
            description = request.POST["txtDescription"]
            #update
            asset_state.code = code
            asset_state.name = name
            asset_state.description = description
            if request.POST.get('ckStatus'):
                asset_state.status = "1"
            else:
                asset_state.status = "0"
            asset_state.parent_id = List.objects.get(id=parent_id,list_type='4')
            check_asset_state = List.objects.exclude(id=state_id).filter(code = code,parent_id = parent_id,list_type='4')
            if len(check_asset_state) >0 :
                context.update({'has_error':'Mã hiện trạng tài sản đã tồn tại'})
            else:
                asset_state.save()
                return HttpResponseRedirect(resolve_url("asset-state"))
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
    return render_to_response("asset/edit-asset-state.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.delete_department',login_url='/permission-error/')
def delete(request,state_id):
    context = {}
    try:
        if request.POST:
            asset_state = List.objects.get(id=state_id,list_type='4')
            childAssetStates = List.objects.filter(parent_id =asset_state.id,list_type='4')
            if len(childAssetStates)>0:
                context.update({'has_error':'Không được phép xóa.Phải xóa các tình trạng sử dụng con trước'})
                states_qs = List.objects.raw("""
                                SELECT id,name,code,description,list_level,status,list_type,
                                    create_datetime,user_name,parent_id,connect_by_isleaf is_leaf
                                FROM list 
                                WHERE list_type='4' 
                                START WITH parent_id IS NULL 
                                CONNECT BY PRIOR id = parent_id 
                                ORDER SIBLINGS BY parent_id 
                                """)
                states = []
                for state in states_qs:
                    row = {}
                    row.update({'id':state.id})
                    row.update({'code':state.code})
                    row.update({'name':state.name})
                    row.update({'description':state.description})
                    row.update({'list_level':state.list_level})
                    row.update({'status':state.status})
                    row.update({'create_date':state.create_datetime.strftime('%Y-%m-%d %H:%M:%S')})
                    row.update({'user_name':state.user_name})
                    try:
                        row.update({'parent_id':state.parent_id.id})
                        row.update({'parent_name':state.parent_id.name})
                        if(state.is_leaf == 1):
                            row.update({'icon':'/tree/css/zTreeStyle/img/diy/8.png'})
                    except:
                        row.update({'open':True,'iconOpen':'/tree/css/zTreeStyle/img/diy/1_open.png', 'iconClose':'/tree/css/zTreeStyle/img/diy/1_close.png'})
                    states.append(row)
                context.update({'data':json.dumps(states,cls=DateEncoder)})
                context.update(csrf(request))
                return render_to_response("asset/asset-state.html", context, RequestContext(request))
            else:
                asset_state.delete()
                return HttpResponseRedirect(resolve_url("asset-state"))
    except Exception as ex:
        context.update({'has_error':str(ex)})
        return HttpResponseRedirect(resolve_url("asset-state"))
