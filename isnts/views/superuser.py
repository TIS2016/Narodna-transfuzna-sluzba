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
    secret_key_change_form = SecretKeyChange(request.POST or None)
    if request.method == 'POST':
        if secret_key_change_form.is_valid():
            employee = Employee.objects.get(id=request.user.id)
            data = secret_key_change_form.cleaned_data
            nts = employee.id_nts
            if data['secret_key_new'] == data['secret_key_new2']:
                nts.secret_key = data['secret_key_new2']
                nts.save()
                return HttpResponseRedirect('/login/')
    return render(request, 'superuser/secret_key_change.html', {'form': secret_key_change_form})


def employee_administration(request):
    employees = Employee.objects.all()
    return render(request, 'superuser/employee_administration.html', {'employees': employees})


def employee_activation(request, employee_id):
    employees = Employee.objects.all()
    employee = get_or_none(Employee, id=employee_id)
    employee_activation_form = EmployeeActivationForm(request.POST or None)
    if request.method == 'POST':
        if employee_activation_form.is_valid():
            data = employee_activation_form.cleaned_data
            if data['activate'] == True:
                employee.is_active = True
                employee.save()
            else:
                employee.is_active = False
                employee.save()
            return HttpResponseRedirect('/superuser/employee_administration', {'employees': employees})
    return render(request, 'superuser/employee_administration_detailview.html', {'form': employee_activation_form, 'employee': employee})
