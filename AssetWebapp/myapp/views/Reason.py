'''
Created on Aug 31, 2014

@author: VinhNDQ
'''
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response

from myapp.models.Reason import Reason
from django.template.context import RequestContext


@login_required(login_url='/login/')
def add_reason(request):
    context ={}
    if request.POST:
        reason_code = request.POST['txtReasonCode']
        reason_name = request.POST['txtReasonName']
        reason_status = request.POST['optStatus']
        description = request.POST['txtDescription']
        try:
            reason = Reason()
            reason.code = reason_code
            reason.name = reason_name
            reason.status=reason_status
            reason.description = description
            reason.save()
            return HttpResponseRedirect("/reason/")
        except Exception as ex:
            context.update({"has_error":str(ex)})
    context.update(csrf(request))
    return render_to_response("reason/add-reason.html",context, RequestContext(request))
@login_required(login_url='/login/')
def view_reason(request):
    reasons = Reason.objects.all().order_by("name")
    context ={"reasons":reasons}
    return render_to_response("reason/reason.html",context, RequestContext(request))
@login_required(login_url='/login/')
def change_reason(request,reason_id):
    try:
        context = {}
        current_reason = Reason.objects.get(id = reason_id)
        context.update({"current_reason":current_reason}) 
        if request.POST :
            try:
                reason_name = request.POST['txtReasonName']
                reason_status = request.POST['optStatus']
                description = request.POST['txtDescription']
                current_reason.reason = reason_name
                current_reason.reason=reason_status
                current_reason.description = description
                current_reason.save()
                return HttpResponseRedirect("/reason/")
            except Exception as ex:
                context.update({'has_error':ex})
        context.update(csrf(request))
        return render_to_response("reason/change-reason.html",context, RequestContext(request))
    except Reason.DoesNotExist:
        return HttpResponseRedirect("/notfound-error")
@login_required(login_url='/login/')
def delete_reason(request,reason_id):
    if request.POST:
        current = Reason.objects.get(id=reason_id)
        current.delete()
    return HttpResponseRedirect("/reason/")