'''
Created on Sep 3, 2014

@author: TuanNA
'''
import datetime
from json import JSONEncoder

class DateEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.strftime('%d/%m/%Y')
        return JSONEncoder.default(self, obj)