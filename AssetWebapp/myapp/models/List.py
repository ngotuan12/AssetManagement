'''
Created on Aug 25, 2014

@author: TuanNA
'''

import datetime

from django.db import models

from myapp.util.sequence import update_id


# Create your models here.
class List(models.Model):
    id = models.IntegerField(primary_key=True,db_column="id")
    code = models.CharField(max_length=10,db_column="code")
    name = models.CharField(max_length=200,db_column="name")
    description = models.CharField(max_length=500,db_column="description")
    parent_id = models.ForeignKey('self',db_column='parent_id')
    list_level = models.CharField(max_length=1,db_column="list_level")
    status = models.CharField(max_length=1,db_column="status")
    interval = models.CharField(max_length=10,db_column="interval")
    class_group = models.CharField(max_length=10,db_column="class_group") 
    list_type = models.CharField(max_length=10,db_column="list_type") 
    create_datetime = models.DateTimeField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),db_column="create_datetime")
    user_name = models.CharField(max_length=20,db_column="user_name")
    parent_code = models.CharField(max_length=40,db_column="parent_code")
    decision_no = models.CharField(max_length=50,db_column="decision_no")
    decisioner = models.CharField(max_length=100,db_column="decisioner")
    #decision_date = models.DateTimeField(default=datetime.datetime.now().strftime('%d-%m-%Y'),db_column="decision_date")   
    decision_date = models.DateTimeField(db_column="decision_date")
    class Meta:
        db_table = 'list'
        app_label = 'myapp'
        permissions = (
            ("view_list", "Can see list"),
        )
    @update_id
    def save(self):
        # Now actually save the object.
        super(List, self).save()