'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')
import datetime
import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
import requests

from myapp.models.Reason import Reason


@login_required(login_url='/login')
def index(request):
	context={}
	print(request.session.get('django_timezone'))
	print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
	reason = Reason()
	reason.reason_code = "dsads"
	reason.reason_name = "test"
	reason.description = "dfds"
# 	reason.create_datetime = datetime.now()
	reason.save()
	context.update(csrf(request))
	return render_to_response("report.html", context)
def test(request):
	authorization = request.session['authorization']
	print(authorization)
	url = 'http://localhost:8080/AssetServer/ReportService'
	payload = {"SessionUserName":"TuanNA","Method":"Test"}
	headers = {'content-type': 'application/json;charset=utf-8',"Authorization":authorization}
	r = requests.request('POST',url, data=json.dumps(payload), headers=headers)
	response = r.json()
	fileout = response['FileOut']
	return HttpResponseRedirect("/report/"+fileout)
def signin(request):
	context ={}
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				url = 'http://localhost:8080/AssetServer/PermissionService'
				payload = {"Method":"login","UserName":"TuanNA","PassWord":"113322"}
				headers = {'content-type': 'application/json;charset=utf-8',"Authorization":""}
				r = requests.request('POST',url, data=json.dumps(payload), headers=headers)
				response = r.json()
				authorization = response['Authorization']
				request.session['authorization'] = authorization;
				login(request, user)
				return HttpResponseRedirect('/home')
			else:
				context.update({'has_error':'User is blocked!'})
		else:
			context.update({'has_error':'Username or password does not correct!'})
	context.update(csrf(request))
	return render_to_response("signin.html", context)
def logout(request):
	logout()