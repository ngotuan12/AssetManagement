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
@permission_required('myapp.view_department',login_url='/permission-error/')
def index(request):
    context = {}
    try:
        goals_qs = List.objects.raw("""
                                SELECT id,name,code,description,list_level,status,list_type,
                                    create_datetime,user_name,parent_id,connect_by_isleaf is_leaf
                                FROM list 
                                WHERE list_type='2' 
                                START WITH parent_id IS NULL 
                                CONNECT BY PRIOR id = parent_id 
                                ORDER SIBLINGS BY parent_id 
                                """)
        goals = []
        for goal in goals_qs:
            row = {}
            row.update({'id':goal.id})
            row.update({'code':goal.code})
            row.update({'name':goal.name})
            row.update({'description':goal.description})
            row.update({'list_level':goal.list_level})
            row.update({'status':goal.status})
            row.update({'create_date':goal.create_datetime.strftime('%Y-%m-%d %H:%M:%S')})
            row.update({'user_name':goal.user_name})
            try:
                row.update({'parent_id':goal.parent_id.id})
                row.update({'parent_name':goal.parent_id.name})
                if(goal.is_leaf == 1):
                    row.update({'icon':'/tree/css/zTreeStyle/img/diy/8.png'})
            except:
                row.update({'open':True,'iconOpen':'/tree/css/zTreeStyle/img/diy/1_open.png', 'iconClose':'/tree/css/zTreeStyle/img/diy/1_close.png'})
            goals.append(row)
        context.update({'data':json.dumps(goals,cls=DateEncoder)})
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
    return render_to_response("goal/goal.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.add_department',login_url='/permission-error/')
def add(request,parent_id):
    context = {}
    try:
        parent = List.objects.get(id=parent_id,list_type='2')
        context.update({'parent_name':parent.name})
        if request.POST:
            code = request.POST["txtCode"]
            name = request.POST["txtName"]
            description = request.POST["txtDescription"]
            goal = List()
            goal.code = code
            goal.name = name
            goal.description = description
            goal.list_type = '2'
            if request.POST.get('ckStatus'):
                goal.status = "1"
            else:
                goal.status = "0"
            goal.parent_id = parent
            goal.user_name = request.user.username
            check_asset_state = List.objects.filter(code = code,parent_id = parent_id,list_type='2')
            if len(check_asset_state) > 0:
                context.update({'has_error':_(u'Mã mục đích sử dụng đã tồn tại')})
                context.update({'goal':goal})
            else:
                goal.save()
                return HttpResponseRedirect(resolve_url("goal"))
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
    return render_to_response("goal/add-goal.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.edit_department',login_url='/permission-error/')
def edit(request,goal_id):
    context = {}
    try:
        goal = List.objects.get(id=goal_id,list_type='2')
        context.update({'parents':List.objects.exclude(id = goal_id).filter(list_type='2')})
        context.update({'goal':goal})
        if request.POST:
            parent_id = request.POST["slParent"]
            code = request.POST["txtCode"]
            name = request.POST["txtName"]
            description = request.POST["txtDescription"]
            #update
            goal.code = code
            goal.name = name
            goal.description = description
            if request.POST.get('ckStatus'):
                goal.status = "1"
            else:
                goal.status = "0"
            goal.parent_id = List.objects.get(id=parent_id,list_type='2')
            check_asset_state = List.objects.exclude(id=goal_id).filter(code = code,parent_id = parent_id,list_type='2')
            if len(check_asset_state) >0 :
                context.update({'has_error':_(u'Mã mục đích sử dụng đã tồn tại')})
            else:
                goal.save()
                return HttpResponseRedirect(resolve_url("goal"))
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
    return render_to_response("goal/edit-goal.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.delete_department',login_url='/permission-error/')
def delete(request,goal_id):
    context = {}
    try:
        if request.POST:
            goal = List.objects.get(id=goal_id,list_type='2')
            childGoals = List.objects.filter(parent_id=goal.id,list_type='2')
            if len(childGoals)>0:
                context.update({'has_error':_(u"Không được phép xóa.Phải xóa các mục đích sử dụng con trước")})
                #get dât
                goals_qs = List.objects.raw("""
                                SELECT id,name,code,description,list_level,status,list_type,
                                    create_datetime,user_name,parent_id,connect_by_isleaf is_leaf
                                FROM list 
                                WHERE list_type='2' 
                                START WITH parent_id IS NULL 
                                CONNECT BY PRIOR id = parent_id 
                                ORDER SIBLINGS BY parent_id 
                                """)
                goals = []
                for goal in goals_qs:
                    row = {}
                    row.update({'id':goal.id})
                    row.update({'code':goal.code})
                    row.update({'name':goal.name})
                    row.update({'description':goal.description})
                    row.update({'list_level':goal.list_level})
                    row.update({'status':goal.status})
                    row.update({'create_date':goal.create_datetime.strftime('%Y-%m-%d %H:%M:%S')})
                    row.update({'user_name':goal.user_name})
                    try:
                        row.update({'parent_id':goal.parent_id.id})
                        row.update({'parent_name':goal.parent_id.name})
                        if(goal.is_leaf == 1):
                            row.update({'icon':'/tree/css/zTreeStyle/img/diy/8.png'})
                    except:
                        row.update({'open':True,'iconOpen':'/tree/css/zTreeStyle/img/diy/1_open.png', 'iconClose':'/tree/css/zTreeStyle/img/diy/1_close.png'})
                    goals.append(row)
                context.update({'data':json.dumps(goals,cls=DateEncoder)})
                context.update(csrf(request))
                return render_to_response("goal/goal.html", context, RequestContext(request))
            else:
                goal.delete()
                context.update({'has_success':_(u"Xóa tài sản thành công")})
                return HttpResponseRedirect(resolve_url("goal"))
    except Exception as ex:
        context.update({'has_error':str(ex)})
        return HttpResponseRedirect(resolve_url("goal"))
