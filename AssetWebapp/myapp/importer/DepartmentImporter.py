'''
Created on Oct 20, 2014

@author: TuanNA
'''
from sc.importer.base import Importer, ImporterColumn


class DepartmentImporter(Importer):
    dept_code = ImporterColumn(column_index=1,column_name="dept_code")
    dept_name = ImporterColumn(column_index=0,column_name="dept_name")
    class Meta:
        table = 'dept'
        package = 'pck_import.department'
        from_row = 1
        db_type= 'oracle'