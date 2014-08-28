'''
Created on Aug 26, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.context_processors import csrf


@login_required(login_url='/login')
def change_password(request):
    return ""
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def reset_password(request):
    return ""
@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def view_user(request):
    users = User.objects.all().order_by("username")
    context ={"users":users}
    return render_to_response("user/user.html",context, RequestContext(request))
@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def add_user(request):
    context ={}
    content_types = ContentType.objects.filter(app_label = "myapp")
    permissions = Permission.objects.filter(content_type__in=content_types).order_by('content_type__id','-codename')
    groups = Group.objects.all()
    if request.POST:
        user_name = request.POST["txtUserName"]
        pass_word = request.POST["txtPassWord"]
        first_name = request.POST["txtFirstName"]
        last_name= request.POST["txtLastName"]
        email = request.POST["txtEmail"]
        try:
            user = User()
            user.username = user_name
            user.set_password(pass_word)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.is_staff = True
            if request.POST.get('checkboxSupperUser'):
                user.is_superuser = True
            else:
                user.is_superuser = False
            if request.POST.get('checkboxActive'):
                user.is_active = True
            else:
                user.is_active = False
            user.save()
            for permission in permissions:
                if request.POST.get('checkboxPer'+str(permission.id)):
                    user.user_permissions.add(permission)
                else:
                    user.user_permissions.remove(permission)
            for group in groups:
                if request.POST.get('checkboxGroup'+str(group.id)):
                    user.groups.add(group)
                else:
                    user.groups.remove(group)
            user.save()
            return HttpResponseRedirect("/user")
        except Exception as ex:
            context.update({"has_error":str(ex)})
    context.update({'permissions':permissions,'groups':groups})
    context.update(csrf(request))
    return render_to_response("user/add-user.html",context, RequestContext(request))
@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def change_user(request,user_id):
    context = {}
    try:
        content_types = ContentType.objects.filter(app_label = "myapp")
        permissions = Permission.objects.filter(content_type__in=content_types).order_by('content_type__id','-codename')
        groups = Group.objects.all()
        current_user = User.objects.get(id=user_id)
        current_pers = current_user.user_permissions.values_list('id', flat=True)
        current_groups = current_user.groups.values_list('id', flat=True)
        context.update({'current_user': current_user,'current_groups':current_groups,'current_pers':current_pers,'permissions':permissions,'groups':groups})
        if request.POST:
#             user_name = request.POST["txtUserName"]
#             pass_word = request.POST["txtPassWord"]
            first_name = request.POST["txtFirstName"]
            last_name= request.POST["txtLastName"]
            email = request.POST["txtEmail"]
            try:
#                 current_user.username = user_name
#                 current_user.set_password(pass_word)
                current_user.first_name = first_name
                current_user.last_name = last_name
                current_user.email = email
                if request.POST.get('checkboxSupperUser'):
                    current_user.is_superuser = True
                else:
                    current_user.is_superuser = False
                if request.POST.get('checkboxActive'):
                    current_user.is_active = True
                else:
                    current_user.is_active = False
                for permission in permissions:
                    if request.POST.get('checkboxPer'+str(permission.id)):
                        current_user.user_permissions.add(permission)
                    else:
                        current_user.user_permissions.remove(permission)
                for group in groups:
                    if request.POST.get('checkboxGroup'+str(group.id)):
                        current_user.groups.add(group)
                    else:
                        current_user.groups.remove(group)
                current_user.save()
                return HttpResponseRedirect("/user")
            except Exception as ex:
                context.update({"has_error":str(ex)})
        context.update(csrf(request))
        return render_to_response("user/change-user.html",context, RequestContext(request))
    except User.DoesNotExist:
        return HttpResponseRedirect("/notfound-error")
@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser,login_url='/permission-error',redirect_field_name=None)
def delete_user(request,user_id):
    if request.POST:
        current_user = User.objects.get(id=user_id)
        current_user.delete()
        return HttpResponseRedirect("/user")