'''
Created on Aug 15, 2014

@author: DienND
'''

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    last_activity_ip = models.IPAddressField(null=True)
    last_activity_date = models.DateTimeField(null=True)
    android_password = models.CharField(null=True,max_length = 200,db_column = 'android_password')
    user = models.OneToOneField(User, primary_key=True)
    class Meta:
        db_table = 'user_profile'