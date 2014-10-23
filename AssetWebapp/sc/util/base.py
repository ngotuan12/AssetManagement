'''
Created on Oct 23, 2014

@author: TuanNA
'''
import datetime
import os

from AssetWebapp.settings import UPLOAD_ROOT

def handle_uploaded_file(f):
    strtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    fileName, fileExtension = os.path.splitext(f.name)
    fileName = fileName + strtime + fileExtension
    with open(UPLOAD_ROOT+"/"+fileName, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return fileName
    