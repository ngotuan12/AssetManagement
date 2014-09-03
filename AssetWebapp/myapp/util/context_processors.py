from myapp.models.Device import Device
def user(request):
    return {
            'user': request.user,
        }
def deviceSummary(request):
    device = Device.objects.all()
    return {
            'summary':{"1":len(device.filter(status = '1')),"0":len(device.filter(status = '0')),"2":len(device.filter(status = '2'))}
        }