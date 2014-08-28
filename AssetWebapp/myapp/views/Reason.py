'''
Created on Aug 26, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response

from myapp.models.Reason import Reason


@login_required(login_url='/login')
@permission_required('myapp.add_reason', raise_exception=True)
def index(request):
    reasons = Reason.objects.all().order_by('id')
    context = {'reasons':reasons}
    context.update(csrf(request))
    return render_to_response("reason.html", context)
@login_required(login_url='/login')
def add_reason(request):
    if(request.POST):
        reason_code = request.POST["txtReasonCode"]
        print(reason_code)
    return HttpResponseRedirect("/reason")
@login_required(login_url='/login')
def update_reason(request):
    return ""
@login_required(login_url='/login')
def delete_reason(request):
    return ""