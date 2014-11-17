'''
Created on Oct 20, 2014

@author: TuanNA
'''
from sc.importer.base import Importer, ImporterColumn


class DepartmentImporter(Importer):
    dept_code = ImporterColumn(column_index=1,column_name="dept_code")
    dept_name = ImporterColumn(column_index=0,column_name="dept_name")
    parent_code = ImporterColumn(column_index=0,column_name="parent_code")
    address = ImporterColumn(column_index=0,column_name="address")
    tel = ImporterColumn(column_index=0,column_name="tel")
    fax = ImporterColumn(column_index=0,column_name="fax")
    contact_persion = ImporterColumn(column_index=0,column_name="contact_person")
    username = ImporterColumn(column_index=0,column_name="username")
    class Meta:
        table = 'dept'
        package = 'pck_import.department'
        from_row = 1
        db_type= 'oracle'