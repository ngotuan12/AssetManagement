'''
Created on Sep 8, 2014

@author: TuanNA
'''
from myapp.models import UserProfile as UserActivity
from datetime import datetime
from django.conf import settings
import re
 
compiledLists = {}
 
class LastActivityMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            return
        urlsModule = __import__(settings.ROOT_URLCONF, {}, {}, [''])
        skipList = getattr(urlsModule, 'skip_last_activity_date', None)
        skippedPath = request.path
        if skippedPath.startswith('/'):
            skippedPath = skippedPath[1:]
        if skipList is not None:
            for expression in skipList:
                compiledVersion = None
                if not compiledLists.has_key(expression):
                    compiledLists[expression] = re.compile(expression)
                compiledVersion = compiledLists[expression]
                if compiledVersion.search(skippedPath):
                    return
        activity = None
        try:
            activity = request.user.useractivity
        except:
            activity = UserActivity()
            activity.user = request.user
            activity.last_activity_date = datetime.now()
            activity.last_activity_ip = request.META['REMOTE_ADDR']
            activity.save()
            return
        activity.last_activity_date = datetime.now()
        activity.last_activity_ip = request.META['REMOTE_ADDR']
        activity.save()