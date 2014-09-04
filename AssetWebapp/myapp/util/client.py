'''
Created on Aug 28, 2014

@author: TuanNA
'''
import json

import requests
from AssetWebapp import settings

def getAuthorization(username):
    url = settings.REPORT_SERVER + settings.PERMISSION_SERVICE
    payload = {"Method":"login","UserName":username,"PassWord":""}
    headers = {'content-type': 'application/json;charset=utf-8',"Authorization":""}
    r = requests.request('POST',url, data=json.dumps(payload), headers=headers)
    response = r.json()
    print(response['Authorization'])
    return response['Authorization']

def exportDeviceReport(authorization,device_id,area_id,device_status):
    url = settings.REPORT_SERVER + settings.REPORT_SERVICE
    payload = {"SessionUserName":"TuanNA","Method":"DeviceReport","device_id":device_id,"area_id":area_id,"device_status":device_status}
    headers = {'content-type': 'application/json;charset=utf-8',"Authorization":authorization}
    r = requests.request('POST',url, data=json.dumps(payload), headers=headers)
    response = r.json()
    fileout = response['FileOut']
    return fileout
def exportDeviceDetailReport(authorization,device_id,area_id,device_status):
    url = settings.REPORT_SERVER + settings.REPORT_SERVICE
    payload = {"SessionUserName":"TuanNA","Method":"DeviceDetailReport","device_id":device_id,"area_id":area_id,"device_status":device_status}
    headers = {'content-type': 'application/json;charset=utf-8',"Authorization":authorization}
    r = requests.request('POST',url, data=json.dumps(payload), headers=headers)
    response = r.json()
    fileout = response['FileOut']
    return fileout
def exportDeviceErrorReport(authorization,device_id,area_id,device_status):
    url = settings.REPORT_SERVER + settings.REPORT_SERVICE
    payload = {"SessionUserName":"TuanNA","Method":"DeviceErrorReport","device_id":device_id,"area_id":area_id,"device_status":device_status}
    headers = {'content-type': 'application/json;charset=utf-8',"Authorization":authorization}
    r = requests.request('POST',url, data=json.dumps(payload), headers=headers)
    response = r.json()
    fileout = response['FileOut']
    return fileout
def exportReportByJasper(authorization,user_name,template_name,params_object,file_type):
    url = settings.REPORT_SERVER + settings.REPORT_SERVICE
    payload = {"SessionUserName":user_name,"Method":"JasperReport","template_name":template_name,"params_object":params_object,"file_type":file_type}
    headers = {'content-type': 'application/json;charset=utf-8',"Authorization":authorization}
    r = requests.request('POST',url, data=json.dumps(payload), headers=headers)
    response = r.json()
    fileout = response['FileOut']
    return fileout
def exportVerifyAsset(authorization,user_name):
    url = settings.REPORT_SERVER + settings.REPORT_SERVICE
    payload = {"SessionUserName":user_name,"Method":"VerifyAssetReport"}
    headers = {'content-type': 'application/json;charset=utf-8',"Authorization":authorization}
    r = requests.request('POST',url, data=json.dumps(payload), headers=headers)
    response = r.json()
    fileout = response['FileOut']
    return fileout