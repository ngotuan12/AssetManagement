# -*- coding: utf-8 -*-
'''
Created on Oct 20, 2014

@author: TuanNA
@copyright: TuanNA
@since: 20/10/2014
'''
import codecs

from django.db import connection
from django.utils.translation import ugettext as _
import xlrd

from AssetWebapp.settings import LOG_ROOT


class Importer(object):
    '''
    Base class of package import
    Use to import data from excel file
    file_path: path of xls file
    import_type:
        1: INSERT TABLE ONLY(default)
        2: INSERT TABLE AND CALL PACKAGE AFTER IMPORT
        3: CALL PACKAGE FOR EACH ROW
    file_type:
        1: xls file
    '''
    def __init__(self, file_path,import_type=1,file_type=1):
        '''
        set attribute file_path
        '''
        setattr(self,"file_path",file_path)
        '''
        set attribute import_type
        '''
        setattr(self,"import_type",import_type)
        '''
        set attribute file_type
        '''
        setattr(self,"file_type",file_type)
        '''
        Analyze column data and set attribute columns
        '''
        attrs= dir(self)
        columns = [getattr(self,attr) for attr in attrs if type(getattr(self,attr)) == ImporterColumn]
        setattr(self,"columns",columns)
        '''
        Build SQL query
        '''
        if hasattr(self.Meta,"table"):
            
            sql = "INSERT INTO %s(" % self.Meta.table
            temp = "VALUES("
            '''
            if database is oracle
            insert id with value = sequence.nextval
            '''
            if hasattr(self.Meta,"db_type") and self.Meta.db_type == "oracle":
                sequence_name = '%s_SEQ' % self.Meta.table
                sql += "id,"
                temp += "%s.nextval," % sequence_name
            for i in range(len(self.columns)):
                if not i == len(self.columns)-1:
                    sql += self.columns[i].column_name + ","
                    temp += "%s,"
                else:
                    sql += self.columns[i].column_name + ")"
                    temp += "%s)"
            sql += temp
            '''
            set attribute sql
            '''
            setattr(self,"sql",sql)
    '''
    Do import
    return log file name
    '''
    def do_import(self):
        '''
        Create cursor
        '''
        cursor = connection.cursor()
        '''
        Create log file
        '''
        log_file = codecs.open(LOG_ROOT+ "\log.txt","w+","utf-8")
        print("Analyze data")
        '''
        read xls file
        '''
        work_book = xlrd.open_workbook(self.file_path)
        sheet = work_book.sheet_by_index(0)
        from_row = 0
        if hasattr(self.Meta,"from_row"):
            from_row = self.Meta.from_row
        to_row = sheet.nrows
        if hasattr(self.Meta,"to_row"):
            to_row = self.Meta.to_row
        for i in range(from_row,to_row):
            values = []
            for j in range(len(self.columns)):
                values.append(sheet.cell_value(i,self.columns[j].column_index))
                print sheet.cell_value(i,self.columns[j].column_index)
            try:
#                     print sql % tuple(values)
                cursor.execute(self.sql,values)
            except Exception as ex:
                log_file.write(_(u"Dòng ") + "%i: %s"% (i,str(ex))+"\n")
#               print _(u"Dòng ") + "%i: %s"% (i,str(ex))
        log_file.close()
    def get_column(self):
        return self.columns
class ImporterColumn(object):
    def __init__(self,column_index, column_name):
        setattr(self,"column_index",column_index)
        setattr(self,"column_name",column_name)