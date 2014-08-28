# -*- coding: utf-8 -*-
'''
Created on Aug 27, 2014

@author: TuanNA
'''
from django.shortcuts import render_to_response
def permission_error(request):
    context = {"has_error": "Bạn không có quyền truy cập vào trang này!"}
    return render_to_response("error.html",context)
def notfound_error(request):
    context = {"has_error": "Trang này không tồn tại!"}
    return render_to_response("error.html",context)
def error(request):
    context = {}
    return render_to_response("error.html",context)