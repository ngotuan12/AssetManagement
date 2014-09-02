'''
Created on Aug 25, 2014

@author: TuanNA
'''

import datetime

from django.db import models

from myapp.util.sequence import update_id


# Create your models here.
class Reason(models.Model):
    id = models.IntegerField(primary_key=True,db_column="id")
    reason_code = models.CharField(max_length=10,db_column="reason_code")
    reason_name = models.CharField(max_length=200,db_column="reason_name")
    reason_status = models.CharField(max_length=1,default='0',db_column="reason_status")
    description = models.CharField(max_length=500,db_column="description")
    group_code = models.CharField(max_length=10,db_column="group_code")
    create_datetime = models.DateTimeField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),db_column="create_datetime")
    user_name = models.CharField(max_length=20,db_column="user_name")
    class Meta:
        db_table = 'reason'
        app_label = 'myapp'
        permissions = (
            ("view_reason", "Can see list reason"),
        )    
    @update_id
    def save(self):
        # Now actually save the object.
        super(Reason, self).save()