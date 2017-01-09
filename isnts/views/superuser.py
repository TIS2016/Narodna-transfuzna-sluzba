from isnts.models import *
from isnts.forms import *
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


@login_required(login_url='/employees/login/')
@permission_required('isnts.is_ntssu', login_url='/nopermission/')
def secret_key_change(request):
    secret_key_change_form = SecretKeyChange(request.POST or None)
    if request.method == 'POST':
        if secret_key_change_form.is_valid():
            employee = Employee.objects.get(id=request.user.id)
            data = secret_key_change_form.cleaned_data
            nts = employee.id_nts
            if data['secret_key_new'] == data['secret_key_new2']:
                nts.secret_key = make_password(data['secret_key_new2'])
                nts.save()
                messages.success(request, 'Secret key has been changed!')
            else:
                messages.success(
                    request, 'Error! Please fill your form with valid values!')

    return render(request, 'superuser/secret_key_change.html', {'form': secret_key_change_form})


@login_required(login_url='/employees/login/')
@permission_required('isnts.is_ntssu', login_url='/nopermission/')
def employee_administration(request):
    employees = Employee.objects.all()
    return render(request, 'superuser/employee_administration.html', {'employees': employees})


@login_required(login_url='/employees/login/')
@permission_required('isnts.is_ntssu', login_url='/nopermission/')
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
