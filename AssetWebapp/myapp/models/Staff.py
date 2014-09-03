'''
Created on Aug 25, 2014

@author: TuanNA
'''

import datetime

from django.db import models

from myapp.util.sequence import update_id


# Create your models here.
class Staff(models.Model):
    id = models.IntegerField(primary_key=True,db_column="staff_id")
    code = models.CharField(max_length=40,db_column="staff_code")
    name = models.CharField(max_length=200,db_column="staff_name")
    dept_code = models.CharField(max_length=40,db_column="dept_code")
    type  = models.CharField(max_length=1,db_column="staff_type")
    status = models.CharField(max_length=1,db_column="staff_status")
    start_date = models.DateTimeField(db_column="sta_date")
    end_date = models.DateTimeField(db_column="end_date")
    create_datetime = models.DateTimeField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),db_column="create_datetime")
    user_name = models.CharField(max_length=20,db_column="user_name")
    class Meta:
        db_table = 'staff'
        app_label = 'myapp'
        permissions = (
            ("view_staff", "Can see list staff"),
        )
    @update_id
    def save(self):
        # Now actually save the object.
        super(Staff, self).save()