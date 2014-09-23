from AdminManagement.models.Module import Module
def user(request):
    return {
            'user': request.user,
        }
def module(request):
    if request.user.is_authenticated():
        modules = Module.objects.raw("""
                                SELECT id,name,code,status,parent_id,
                                connect_by_isleaf is_leaf 
                                FROM module
                                WHERE app_id= 1
                                AND type IN ('M','G')
                                START WITH parent_id IS NULL 
                                CONNECT BY PRIOR id = parent_id 
                                ORDER SIBLINGS BY ord 
                                """)
        return {'modules':modules}
    else:
        return {}
