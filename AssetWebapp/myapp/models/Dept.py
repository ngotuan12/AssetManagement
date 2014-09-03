'''
Created on Aug 25, 2014

@author: TuanNA
'''

import datetime

from django.db import models

from myapp.util.sequence import update_id


# Create your models here.
class Dept(models.Model):
    id = models.IntegerField(primary_key=True,db_column="id")
    code = models.CharField(max_length=10,db_column="dept_code")
    name = models.CharField(max_length=200,db_column="dept_name")
    parent_id = models.ForeignKey('self',db_column='parent_id')
    address = models.CharField(max_length=300,db_column="address")
    tel = models.CharField(max_length=100,db_column="tel")
    fax = models.CharField(max_length=100,db_column="fax")
    contact_person = models.CharField(max_length=200,db_column="contact_person")
    status = models.CharField(max_length=1,db_column="dept_status")
    create_datetime = models.DateTimeField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),db_column="create_datetime")
    user_name = models.CharField(max_length=20,db_column="user_name")
    parent_code = models.CharField(max_length=40,db_column="parent_code")
    class Meta:
        db_table = 'dept'
        app_label = 'myapp'
        permissions = (
            ("view_dept", "Can see list dept"),
        )
    @update_id
    def save(self):
        # Now actually save the object.
        super(Dept, self).save()