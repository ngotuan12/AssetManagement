'''
Created on Aug 28, 2014

@author: TuanNA
@since: 28/08/2014
@version: 1.0
@note: Class do communicate with report server
'''
import json

import requests
from AssetWebapp import settings
def getAuthorization(username):
    url = settings.REPORT_SERVER + settings.PERMISSION_SERVICE
    payload = {"Method":"login","UserName":username,"PassWord":""}
    headers = {'content-type': 'application/json;charset=utf-8',"Authorization":""}
    dataResponse = requests.request('POST',url, data=json.dumps(payload), headers=headers)
    response = processResponse(dataResponse)
    return response['Authorization']
def exportReportByJasper(authorization,user_name,template_name,params_object,file_type):
    url = settings.REPORT_SERVER + settings.REPORT_SERVICE
    payload = {"SessionUserName":user_name,"Method":"JasperReport","template_name":template_name,"params_object":params_object,"file_type":file_type}
    headers = {'content-type': 'application/json;charset=utf-8',"Authorization":authorization}
    dataResponse = requests.request('POST',url, data=json.dumps(payload), headers=headers)
    response = processResponse(dataResponse)
    fileout = response['FileOut']
    return fileout
def exportVerifyAsset(authorization,user_name):
    url = settings.REPORT_SERVER + settings.REPORT_SERVICE
    payload = {"SessionUserName":user_name,"Method":"VerifyAssetReport"}
    headers = {'content-type': 'application/json;charset=utf-8',"Authorization":authorization}
    dataResponse = requests.request('POST',url, data=json.dumps(payload), headers=headers)
    response = processResponse(dataResponse)
    fileout = response['FileOut']
    return fileout
def exportAssetByProjectReport(authorization,project_id,user_name):
    url = settings.REPORT_SERVER + settings.REPORT_SERVICE
    payload = {"SessionUserName":user_name,"Method":"AssetByProjectReport","project_id":project_id}
    headers = {'content-type': 'application/json;charset=utf-8',"Authorization":authorization}
    dataResponse = requests.request('POST',url, data=json.dumps(payload), headers=headers)
    response = processResponse(dataResponse)
    fileout = response['FileOut']
    return fileout
def processResponse(dataResponse):
    response = dataResponse.json()
    if response['handle'] == "on_error":
        raise Exception(response['message'])
    return response