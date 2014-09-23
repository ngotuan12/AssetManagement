# -*- coding: utf-8 -*-
'''
Created on Sep 12, 2014

@author: vinhndq
'''
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.util.DateEncoder import DateEncoder
from myapp.models.Asset import Asset
from django.core.context_processors import csrf

@login_required(login_url='/login/')
@permission_required('myapp.view_asset_type', login_url='/permission-error/')
def index(request):
    context={}
    try:
        '''
        if request.POST:
            action_type=request.POST['action_type'].strip()
            asset_type_id=request.POST['asset_id'].strip()
            asset_type_code=request.POST['asset_code'].strip()
            asset_type_name=request.POST['asset_name'].strip()
            asset_type_parent=request.POST['asset_parent'].strip()
            asset_type_description=request.POST['asset_description'].strip()
            if(action_type=='delete'):
                current = Asset.objects.get(id=asset_type_id)
                childrends=Asset.objects.filter(parent_id=current)
                for child in childrends:
                    child.delete()
                current.delete()
                context.update({"has_success":"Xóa thành công!"})
            elif action_type=='add':
                check_asset=Asset.objects.filter(code=asset_type_code).count()
                if(check_asset>0):
                    context.update({'has_error':'Mã tài sản đã tồn tại'})
                else:
                    asset=Asset()
                    asset.code=asset_type_code
                    asset.name=asset_type_name
                    asset.user_name=request.user.username
                    if (asset_type_parent!=''):
                        asset_parent=Asset.objects.get(id=int(asset_type_parent))
                        if(asset_parent is not None):
                            asset.parent_id=asset_parent
                            asset.parent_code=asset_parent.code
                    asset.description=asset_type_description
                    asset.save()
                    context.update({"has_success":"Thêm mới thành công!"})
            else:
                asset_type_id=asset_type_id.strip()
                check_asset=Asset.objects.filter(code=asset_type_code).exclude(id=asset_type_id).count()
                if(check_asset>0):
                    context.update({'has_error':'Mã tài sản đã tồn tại'})
                else:
                    asset=Asset.objects.get(id=asset_type_id)
                    asset.code=asset_type_code
                    asset.name=asset_type_name
                    if (asset_type_parent==''):
                        asset.parent_id=None
                        asset.parent_code=None
                    else:
                        asset_parent=Asset.objects.get(id=int(asset_type_parent))
                        asset.parent_id=asset_parent
                        if(asset_parent is not None):
                            asset.parent_code=asset_parent.code
                        else:
                            asset.parent_code=None
                    asset.description=asset_type_description
                    asset.save()
                    context.update({"has_success":"Cập nhật thông tin thành công!"})
        '''
        assets=Asset.objects.raw("""
                                SELECT id,name,code,nvl(status,'1') status,parent_code,
                                    description,create_datetime,user_name,interval,account_no,
                                    parent_id,connect_by_isleaf is_leaf 
                                FROM asset 
                                START WITH parent_id IS NULL 
                                CONNECT BY PRIOR id = parent_id 
                                ORDER SIBLINGS BY name 
                                """)
        infors=[]
        infors.append({'id':None,'parent_id':-1,'name':'Loại tài sản cố định','iconOpen':'/tree/css/zTreeStyle/img/diy/1_open.png', 'iconClose':'/tree/css/zTreeStyle/img/diy/1_close.png'})
        for asset in assets:
            row={}
            row.update({'id':asset.id})
            row.update({'name':asset.name})
            row.update({'code':asset.code})
            row.update({'status':asset.status})
            row.update({'description':asset.description})
            row.update({'create_date':asset.create_datetime})
            row.update({'user_name':asset.user_name})
            row.update({'account_no':asset.account_no})
            row.update({'interval':asset.interval})
            if asset.parent_id is not None:
                row.update({'parent_id':asset.parent_id.id})
                row.update({'parent_name':asset.parent_id.name})
            else:
                row.update({'parent_id':None})
                row.update({'parent_name':'Loại tài sản cố định'})
            if(asset.is_leaf == 1):
                row.update({'icon':'/tree/css/zTreeStyle/img/diy/8.png'})
            infors.append(row)
        context.update({"data":json.dumps(infors,cls=DateEncoder)})
        #context.update({"asset_parents":assets})
    except Exception as ex:
        context.update({'has_error':str(ex)})
    return render_to_response("asset-type/asset-type.html",context,RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.add_asset_type', login_url='/permission-error/')
def add_asset_type(request,parent_id):
    context = {}
    try:
        parents = Asset.objects.filter(id=parent_id)
        parent=None
        if(parents.count()<=0):
            context.update({'parent_name':'---Không thuộc loại tài sản nào---'})
            parent=None
        else:
            parent=parents[0]
            context.update({'parent_name':parent.name})
        if request.POST:
            asset_code = request.POST["txtCode"]
            name = request.POST["txtName"]
            description = request.POST["txtDescription"]
            account_no = request.POST["txtAccountNo"]
            interval = request.POST["txtInterval"]
            check_asset=Asset.objects.filter(code=asset_code).count()
            if(check_asset>0):
                context.update({'has_error':'Mã tài sản đã tồn tại'})
            else:
                asset = Asset()
                asset.code = asset_code
                asset.name = name
                asset.description = description
                asset.account_no = account_no
                asset.interval = interval
                if request.POST.get('ckStatus'):
                    asset.status = "1"
                else:
                    asset.status = "0"
                asset.parent_id = parent
                if(parent is not None):
                    asset.parent_code=parent.code
                asset.user_name=request.user.username
                asset.save()
                return HttpResponseRedirect("/asset-type/")
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
    return render_to_response("asset-type/add-asset-type.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.edit_asset_type', login_url='/permission-error/')
def edit_asset_type(request,asset_id):
    context = {}
    try:
        current=Asset.objects.get(id=asset_id)
        context.update({'parents':Asset.objects.exclude(id=asset_id)})
        context.update({'asset':current})
        if request.POST:
            parent_id = request.POST["slParent"]
            asset_code = request.POST["txtCode"]
            name = request.POST["txtName"]
            description = request.POST["txtDescription"]
            account_no = request.POST["txtAccountNo"]
            interval = request.POST["txtInterval"]
            check_asset=Asset.objects.filter(code=asset_code).exclude(id=asset_id).count()
            if(check_asset>0):
                context.update({'has_error':'Mã tài sản đã tồn tại'})
            else:
                current.code = asset_code
                current.name = name
                current.description = description
                current.account_no = account_no
                current.interval = interval
                if request.POST.get('ckStatus'):
                    current.status = "1"
                else:
                    current.status = "0"
                parents=Asset.objects.filter(id=parent_id)
                parent=None
                current.parent_code=None
                if(parents.count()>0):
                    parent=parents[0]
                    current.parent_code=parent.code
                current.parent_id = parent
                current.save()
                return HttpResponseRedirect("/asset-type/")
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
    return render_to_response("asset-type/edit-asset-type.html", context, RequestContext(request))
@login_required(login_url='/login/')
@permission_required('myapp.delete_asset_type',login_url='/permission-error/')
def delete(request,asset_id):
    context = {}
    try:
        if request.POST:
            asset = Asset.objects.get(id=asset_id)
            asset.delete()
            return HttpResponseRedirect("/asset-type/")
    except Exception as ex:
        context.update({'has_error':str(ex)})
        return HttpResponseRedirect("/asset-type/")
@login_required(login_url='/login/')
@permission_required('myapp.asset_type', login_url='/permission-error/')
def load_asset_detail(request,asset_id):
    try:
        assets=Asset.objects.filter(id=asset_id)
        infors=[]
        for asset in assets:
            infors.append(model_to_dict(asset))
        return HttpResponse(json.dumps({"asset_detail":infors},cls=DateEncoder),content_type="application/json")
    except Exception as ex:
        return HttpResponse(json.dumps({"error":str(ex)},cls=DateEncoder),content_type="application/json")
