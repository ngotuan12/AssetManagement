# -*- coding: utf-8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response, resolve_url
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from AdminManagement.models.App import App
from AdminManagement.models.Module import Module
@login_required(login_url='/login/')
@permission_required('myapp.view_app', login_url='/permission-error/')
def index(request):
    context = {}
    try:
        apps = App.objects.all().order_by('status')
        context.update({'apps':apps})
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
        return render_to_response("app/list-app.html", context, RequestContext(request))
def edit_app(request,app_id):
    try:
        context = {}
        app = App.objects.get(id = app_id)
        context.update({"app":app}) 
        if request.POST :
            try:
                app_code = request.POST['txtCode']
                app_name = request.POST['txtName']
                app_type = '1'
                app_status = request.POST['slStatus']
                app_createDate = datetime.strptime(request.POST['dt_app'],'%d/%M/%Y')
                username = request.user.username
                
                app.code = app_code
                app.name = app_name
                app.type = app_type
                app.status = app_status
                
                module =Module.objects.get(app = app_id)
                
                module.code = app_code
                module.name =app_name
                module.status = app_status
                module.user_name = username
                
                check_app=App.objects.exclude(id = app_id).filter(code=app_code)
                if(len(check_app) > 0):
                    context.update({'has_error':_(u'Mã ứng dụng đã tồn tại')})
                else:
                    app.save()
                    module.save()
                    return HttpResponseRedirect(resolve_url("app"))
            except Exception as ex:
                context.update({'has_error':ex})
        context.update(csrf(request))
        return render_to_response("app/edit-app.html",context, RequestContext(request))
    except App.DoesNotExist:
        return HttpResponseRedirect("/notfound-error")
def add_app(request):
    try:
        context = {}
        if request.POST :
            try:
                app_code = request.POST['txtCode']
                app_name = request.POST['txtName']
                app_type = '1'
                app_status = request.POST['slStatus']
                app_createDate = datetime.strptime(request.POST['dt_app'],'%d/%M/%Y')
                username = request.user.username
                app = App()
                
                app.code = app_code
                app.name = app_name
                app.type = app_type
                app.status = app_status
                
                module =Module()
                
                module.code = app_code
                module.name =app_name
                module.type = 'R'
                module.status = app_status
                module.user_name = username
                module.create_date = app_createDate
                
                check_app=App.objects.filter(code=app_code)
                if(len(check_app) > 0):
                    context.update({'has_error':_(u'Mã ứng dụng đã tồn tại')})
                    context.update({'app':app})
                else:
                    app.save()
                    
                    module.app = app
                    module.save()
                    return HttpResponseRedirect(resolve_url("app"))
            except Exception as ex:
                context.update({'has_error':ex})
        context.update(csrf(request))
        return render_to_response("app/add-app.html",context, RequestContext(request))
    except App.DoesNotExist:
        return HttpResponseRedirect("/notfound-error")
@login_required(login_url='/login/')
def delete_app(request,app_id):
    try:
        try:
            context = {}
            app = App.objects.get(id=app_id)
            modules = Module.objects.filter(app=app_id)
            if len(modules) == 0 :
                app.delete()
                return HttpResponseRedirect(resolve_url("app"))
                context.update({'has_success':_(u"Ứng dụng đã được xóa")})
            elif len(modules) == 1 :
                chilModules = Module.objects.filter(parent = modules[0].id)
                if len(chilModules) > 0:
                    context.update({'has_error':_(u'Không được phép xóa ứng dụng này')})
                else:
                    modules[0].delete()
                    app.delete()
                    return HttpResponseRedirect(resolve_url("app"))
                    context.update({'has_success':_(u"Ứng dụng đã được xóa")})
            elif len(modules) > 1 :
                context.update({'has_error':_(u'Không được phép xóa ứng dụng này')})
        except Exception as ex:
            context.update({'has_error':ex})
        finally:
            apps = App.objects.all().order_by('status')
            context.update({'apps':apps})
            context.update(csrf(request))
            return render_to_response("app/list-app.html",context, RequestContext(request))
    except App.DoesNotExist:
            return HttpResponseRedirect("/notfound-error")