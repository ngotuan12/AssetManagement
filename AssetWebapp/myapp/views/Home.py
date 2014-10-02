# -*- coding: utf-8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.Asset import Asset


@login_required(login_url='/login/')
def index(request):
	context={}
	response =  render_to_response("index.html", context, RequestContext(request))
	return response
@login_required(login_url='/login/')
def invoice(request):
	context={}
	return render_to_response("invoice.html", context, RequestContext(request))
@login_required(login_url='/login/')
def tree(request):
		assets = Asset.objects.raw("select id, NAME,code,parent_code,parent_id "+
									"FROM asset "+ 
									"start with parent_id is null "+
									"connect by prior id = parent_id ORDER BY code ")
		infors =[]
		for asset in assets:
			try:
				infors.append({'id':asset.id,'pId':asset.parent_id.id,'name':asset.name})
			except Asset.DoesNotExist:
				infors.append({'id':asset.id,'pId':None,'name':asset.name})
		context={'assets':assets,'data':json.dumps(infors)}
		return render_to_response("tree.html", context, RequestContext(request))
