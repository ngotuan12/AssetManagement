'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')
import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
import requests

from myapp.models import Device


@login_required(login_url='/login')
def index(request):
	devices = Device.objects.all()
	context={'devices':devices}
	return render_to_response("index.html", context)
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
				print(response['Authorization'])
				url = 'http://localhost:8080/AssetServer/ReportService'
				payload = {"SessionUserName":"TuanNA","Method":"Test"}
				headers = {'content-type': 'application/json;charset=utf-8',"Authorization":response['Authorization']}
				r = requests.request('POST',url, data=json.dumps(payload), headers=headers)
				response = r.json()
				fileout = response['FileOut']
				print(fileout)
				login(request, user)
				return HttpResponseRedirect('/report/'+fileout)
			else:
				context.update({'has_error':'User is blocked!'})
		else:
			context.update({'has_error':'Username or password does not correct!'})
	context.update(csrf(request))
	return render_to_response("signin.html", context)
def logout(request):
	logout()