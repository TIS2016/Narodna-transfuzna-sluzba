from isnts.models import *
from isnts.forms import *
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect



def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def secret_key_change(request):
    if request.user.is_authenticated():
        id_nts = request.employee.id_nts
        nts = get_or_none(NTS, id=id_nts)


    secret_key_change_form = SecretKeyChange()
    if request.method == 'POST':
        if secret_key_change_form.is_valid():
            secret_key_change_form.save()
            return HttpResponseRedirect('/login/')
    return render(request, 'superuser/secret_key_change.html', {'form': secret_key_change_form})


def employee_administration(request):
    employees = Employee.objects.all()
    nts = NTS.objects.all()
    return render(request, 'superuser/employee_administration.html', {'employees': employees, 'nts': nts})


def employee_activation(request, employee_id):
    employees = Employee.objects.all()
    employee = get_or_none(Employee, id=employee_id)
    if employee.is_active:
        employee.is_active = False
        employee.save()
    else:
        employee.is_active = True
        employee.save()
    return render(request, 'superuser/employee_administration.html', {'employees': employees})
