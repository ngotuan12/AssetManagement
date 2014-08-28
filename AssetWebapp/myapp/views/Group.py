'''
Created on Aug 26, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import  Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext


@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def view_group(request):
    groups = Group.objects.all().order_by("name")
    context ={"groups":groups}
    return render_to_response("group/group.html",context, RequestContext(request))
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def add_group(request):
    content_types = ContentType.objects.filter(app_label = "myapp")
    permissions = Permission.objects.filter(content_type__in=content_types).order_by('content_type__id','-codename')
    context = {}
    if request.POST :
        try:
            group_name = request.POST['txtGroupName']
            group = Group()
            group.name = group_name
            group.save()
            for permission in permissions:
                if request.POST.get('checkboxPer'+str(permission.id)):
                    group.permissions.add(permission)
                else:
                    group.permissions.remove(permission)
            return HttpResponseRedirect("/group")
        except Exception as ex:
            context.update({'has_error':ex})
    context.update({'permissions':permissions})
    context.update(csrf(request))
    return render_to_response("group/add-group.html",context, RequestContext(request))
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def change_group(request,group_id):
    try:
        context = {}
        current_group = Group.objects.get(id = group_id)
        content_types = ContentType.objects.filter(app_label = "myapp")
        permissions = Permission.objects.filter(content_type__in=content_types).order_by('content_type__id','-codename')
        current_pers= current_group.permissions.values_list('id', flat=True)
        if request.POST :
            try:
                group_name = request.POST['txtGroupName']
                current_group.name = group_name
                for permission in permissions:
                    if request.POST.get('checkboxPer'+str(permission.id)):
                        current_group.permissions.add(permission)
                    else:
                        current_group.permissions.remove(permission)
                current_group.save()
                return HttpResponseRedirect("/group")
            except Exception as ex:
                context.update({'has_error':ex})
        context.update({'permissions':permissions,'current_group':current_group,'current_pers':current_pers})
        context.update(csrf(request))
        return render_to_response("group/change-group.html",context, RequestContext(request))
    except Group.DoesNotExist:
        return HttpResponseRedirect("/notfound-error")
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def delete_group(request,group_id):
    if request.POST :
        current_group = Group.objects.get(id = group_id)
        current_group.delete()
    return HttpResponseRedirect("/group")