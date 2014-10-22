'''
Created on Oct 22, 2014

@author: TuanNA
'''
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def index(request):
    context = {}
    return render_to_response("asset/import-asset.html", context, RequestContext(request))