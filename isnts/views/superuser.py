from isnts.models import *
from isnts.forms import *
from django.shortcuts import render


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def secret_key_change(request):
    secret_key_change_form = SecretKeyChange()
    if request.method == 'POST':
        if secret_key_change_form.is_valid():
            secret_key_change_form.save()
            update_session_auth_hash(request, password_change_form.user)
            return HttpResponseRedirect('/login/')
    return render(request, 'superuser/secret_key_change.html', {'form': secret_key_change_form})


def employee_administration(request):
    employees = Employee.objects.all()
    return render(request, 'superuser/employee_administration.html', {'employees': employees})


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
