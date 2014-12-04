# -*- coding: utf-8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''
import cx_Oracle
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.db import connection
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from myapp.models.Dept import Dept
from myapp.models.List import List
from myapp.models.Stock import Stock

@login_required(login_url='/login/')
@permission_required('myapp.upgrade_asset', login_url='/permission-error/')
def index(request):
    context = {}
    try:
        context.update({'depts':Dept.objects.all()})
        context.update({'stocks':Stock.objects.all()})
        context.update({'goals':List.objects.filter(list_type='2')})
        context.update({'states':List.objects.filter(list_type='4')})
        if request.POST: 
            # Get parameter
            p_serial = request.POST["slSerial"]
            cost_amount = request.POST["hd_cost_amount"]
            interval = request.POST["txtInterval"]
            username = request.user.username
            state_id = request.POST["slState"]
            goad_id = request.POST["slGoal"]
            note = request.POST["txtNote"]
            
            decisionNo = request.POST["txtDecisionNo"]
            decisionName = request.POST["txtDecisionName"]
            decisionDate = request.POST["dtDecisionDate"]
            
            cursor = connection.cursor()
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'DD/MM/YYYY HH24:MI:SS.FF'")
            p_error = cursor.var(cx_Oracle.STRING).var
            cursor.callproc("pck_asset.upgrade_asset",
                        (
                            #p_error
                            p_error,
                            #p_serial
                            p_serial,
                            #p_cost_amount
                            cost_amount,
                            #p_interval
                            interval,
                            #p_state_id
                            state_id,
                             #p_goal_id
                            goad_id,
                            #p_note
                            note,
                            #p_username
                            username,
                            #p_decision_no
                            decisionNo,
                            #p_decisioner
                            decisionName,
                            #p_decision_date
                            decisionDate
                        ))
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' "  
                                       "NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")
            cursor.close()
            if p_error.getvalue() is not None:
                raise Exception(p_error.getvalue())
            context.update({'has_success':_(u"Nâng cấp tài sản thành công")})
    except Exception as ex:
        context.update({'has_error':str(ex)})
    finally:
        context.update(csrf(request))
        return render_to_response("asset/upgrade-asset.html", context, RequestContext(request))