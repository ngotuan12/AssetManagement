# -*- coding: utf-8 -*-
'''
Created on Aug 27, 2014

@author: TuanNA
'''
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response
def permission_error(request):
    context = {"has_error": _(u"Bạn không có quyền truy cập vào trang này!")}
    return render_to_response("error.html",context)
def notfound_error(request):
    context = {"has_error": _(u"Trang này không tồn tại!")}
    return render_to_response("error.html",context)
def error(request):
    has_error = _(u"Lỗi xảy ra")
    if request.GET.get("error"):
        has_error = request.GET.get("error")
    context = {"has_error":has_error}
    return render_to_response("error.html",context)