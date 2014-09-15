# -*- coding: utf-8 -*-
'''
Created on Sep 12, 2014

@author: vinhndq
'''
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.util.DateEncoder import DateEncoder
from myapp.models.Asset import Asset
from datetime import datetime

@login_required(login_url='/login/')
@permission_required('myapp.asset_type', login_url='/permission-error/')
def index(request):
    context={}
    try:
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
        assets=Asset.objects.all().order_by("name")
        infors=[]
        for asset in assets:
            if asset.parent_id is not None:
                infors.append({"id":asset.id,"pId":asset.parent_id.id,"name":asset.name})
            else:
                infors.append({"id":asset.id,"pId":None,"name":asset.name})
        context.update({"data":json.dumps(infors)})
        context.update({"asset_parents":assets})
    except Exception as ex:
        context.update({'has_error':str(ex)})
    return render_to_response("asset/asset-type.html",context,RequestContext(request))
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
