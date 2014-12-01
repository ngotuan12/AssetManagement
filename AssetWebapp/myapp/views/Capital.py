# -*- coding: utf-8 -*-

import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response, resolve_url
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from myapp.models.List import List
from myapp.util.DateEncoder import DateEncoder


@login_required(login_url='/login/')
@permission_required('myapp.view_capital',login_url='/permission-error/')
def index(request):
    context = {}
    try:
        capitals_qs = List.objects.raw("""
                                SELECT id,name,code,description,list_level,status,list_type,
                                    create_datetime,user_name,parent_id,connect_by_isleaf is_leaf
                                FROM list 
                                WHERE list_type='3' 
                                START WITH parent_id IS NULL 
                                CONNECT BY PRIOR id = parent_id 
                                ORDER SIBLINGS BY parent_id 
                                """)
        capitals = []
        for capital in capitals_qs:
            row = {}
            row.update({'id':capital.id})
            row.update({'code':capital.code})
            row.update({'name':capital.name})
            row.update({'description':capital.description})
            row.update({'list_level':capital.list_level})
            row.update({'status':capital.status})
            row.update({'create_date':capital.create_datetime.strftime('%Y-%m-%d %H:%M:%S')})
            row.update({'user_name':capital.user_name})
            try:
                row.update({'parent_id':capital.parent_id.id})
                row.update({'parent_name':capital.parent_id.name})
                if(capital.is_leaf == 1):
                    row.update({'icon':'/tree/css/zTreeStyle/img/diy/8.png'})
            except:
                row.update({'open':True,'iconOpen':'/tree/css/zTreeStyle/img/diy/1_open.png', 'iconClose':'/tree/css/zTreeStyle/img/diy/1_close.png'})
            capitals.append(row)
        context.update({'data':json.dumps(capitals,cls=DateEncoder)})
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
    return render_to_response("capital/capital.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.add_capital',login_url='/permission-error/')
def add(request,parent_id):
    context = {}
    try:
        parent = List.objects.get(id=parent_id,list_type='3')
        context.update({'parent_name':parent.name})
        if request.POST:
            code = request.POST["txtCode"]
            name = request.POST["txtName"]
            description = request.POST["txtDescription"]
            capital = List()
            capital.code = code
            capital.name = name
            capital.description = description
            capital.list_type = '3'
            if request.POST.get('ckStatus'):
                capital.status = "1"
            else:
                capital.status = "0"
            capital.parent_id = parent
            capital.user_name = request.user.username
            check_asset_state = List.objects.filter(code = code,parent_id = parent_id,list_type='3')
            if len(check_asset_state) > 0:
                context.update({'has_error':_(u'Mã nguồn vốn đã tồn tại')})
                context.update({'capital':capital})
            else:
                capital.save()
                return HttpResponseRedirect(resolve_url("capital"))
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
    return render_to_response("capital/add-capital.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.edit_capital',login_url='/permission-error/')
def edit(request,capital_id):
    context = {}
    try:
        capital = List.objects.get(id=capital_id,list_type='3')
        context.update({'parents':List.objects.exclude(id = capital_id).filter(list_type='3')})
        context.update({'capital':capital})
        if request.POST:
            parent_id = request.POST["slParent"]
            code = request.POST["txtCode"]
            name = request.POST["txtName"]
            description = request.POST["txtDescription"]
            #update
            capital.code = code
            capital.name = name
            capital.description = description
            if request.POST.get('ckStatus'):
                capital.status = "1"
            else:
                capital.status = "0"
            capital.parent_id = List.objects.get(id=parent_id,list_type='3')
            check_asset_state = List.objects.exclude(id=capital_id).filter(code = code,parent_id = parent_id,list_type='3')
            if len(check_asset_state) >0 :
                context.update({'has_error':_(u'Mã nguồn vốn đã tồn tại')})
            else:
                capital.save()
                return HttpResponseRedirect(resolve_url("capital"))
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
    return render_to_response("capital/edit-capital.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.delete_capital',login_url='/permission-error/')
def delete(request,capital_id):
    context = {}
    try:
        if request.POST:
            capital = List.objects.get(id=capital_id,list_type='3')
            childcapitals = List.objects.filter(parent_id=capital.id,list_type='3')
            if len(childcapitals)>0:
                context.update({'has_error':_(u"Không được phép xóa.Phải xóa các nguồn vốn con trước")})
                #get dât
                capitals_qs = List.objects.raw("""
                                SELECT id,name,code,description,list_level,status,list_type,
                                    create_datetime,user_name,parent_id,connect_by_isleaf is_leaf
                                FROM list 
                                WHERE list_type='3' 
                                START WITH parent_id IS NULL 
                                CONNECT BY PRIOR id = parent_id 
                                ORDER SIBLINGS BY parent_id 
                                """)
                capitals = []
                for capital in capitals_qs:
                    row = {}
                    row.update({'id':capital.id})
                    row.update({'code':capital.code})
                    row.update({'name':capital.name})
                    row.update({'description':capital.description})
                    row.update({'list_level':capital.list_level})
                    row.update({'status':capital.status})
                    row.update({'create_date':capital.create_datetime.strftime('%Y-%m-%d %H:%M:%S')})
                    row.update({'user_name':capital.user_name})
                    try:
                        row.update({'parent_id':capital.parent_id.id})
                        row.update({'parent_name':capital.parent_id.name})
                        if(capital.is_leaf == 1):
                            row.update({'icon':'/tree/css/zTreeStyle/img/diy/8.png'})
                    except:
                        row.update({'open':True,'iconOpen':'/tree/css/zTreeStyle/img/diy/1_open.png', 'iconClose':'/tree/css/zTreeStyle/img/diy/1_close.png'})
                    capitals.append(row)
                context.update({'data':json.dumps(capitals,cls=DateEncoder)})
                context.update(csrf(request))
                return render_to_response("capital/capital.html", context, RequestContext(request))
            else:
                capital.delete()
                context.update({'has_success':_(u"Xóa nguồn vốn thành công")})
                return HttpResponseRedirect(resolve_url("capital"))
    except Exception as ex:
        context.update({'has_error':str(ex)})
        return HttpResponseRedirect(resolve_url("capital"))
