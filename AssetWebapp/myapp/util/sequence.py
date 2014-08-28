'''
Created on Aug 25, 2014

@author: TuanNA
'''
def update_id(func):
    '''A decorator for pulling a data object's ID value out of a
       user-defined sequence.  This gets around a limitation in 
       django whereby we cannot supply our own sequence names.'''
     
    def decorated_function(*args):
        # Grab a reference to the data object we want to update.
        data_object = args[0]
         
        # Only update the ID if there isn't one yet.
        if data_object.id is None:
            # Construct the new sequence name based on the table's meta data.
            sequence_name = '%s_SEQ' % data_object._meta.db_table
            print (sequence_name)
            # Query the database for the next sequence value.
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("SELECT %s.nextval FROM dual" % sequence_name)
            row = cursor.fetchone()
            # Update the data object's ID with the returned sequence value.
            data_object.id = row[0]
            cursor.close()
        # Execute the function we're decorating.
        return func(*args)
    return decorated_function