from isnts.models import *
from isnts.forms import *
from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.core.exceptions import ObjectDoesNotExist


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


@login_required(login_url='/employees/login/')
@permission_required('isnts.is_employee', login_url='/nopermission/')
def listview(request):
    employees = Employee.objects.filter(groups__name__in=['Doctor','Nurse'])
    return render(request, 'employees/listview.html', {'employees': employees})


def is_ntssu(user):
    g = Group.objects.get(name='NTSsu')
    return g in user.groups.all()


@login_required(login_url='/employees/login/')
@permission_required('isnts.is_employee', login_url='/nopermission/')
@user_passes_test(is_ntssu, login_url='/nopermission/')
def detailview(request, employee_id):
    user = get_or_none(Employee, id=request.user.id)
    employee = get_or_none(Employee, id=employee_id)
    if employee is None:
        raise ObjectDoesNotExist
    if user.id_nts is not None and employee.id_nts is not None and user.id_nts.id != employee.id_nts.id:
        return HttpResponseRedirect('/nopermission/')
    e_types = [('', '---------')]
    e_types += list((int(g.id), g.name)
                    for g in Group.objects.exclude(name='NTSsu').exclude(name='Donor'))
    if request.method == 'POST':
        employee_form = EmployeeRegister(
            request.POST, instance=employee, emp_types=e_types)
        if employee_form.is_valid():
            new_g = Group.objects.get(
                id=employee_form.cleaned_data['employee_type'])
            old_g = employee.groups.all()[0]
            old_g.user_set.remove(employee)
            new_g.user_set.add(employee)
            employee_form.save()
            return render(request, 'employees/detailview.html', {'form': employee_form})
    else:
        employee_form = EmployeeRegister(instance=employee, emp_types=e_types)
    employee_form.fields['employee_type'].initial = employee.groups.all()[0].id
    return render(request, 'employees/detailview.html', {'form': employee_form})


@login_required(login_url='/employees/login/')
@permission_required('isnts.is_employee', login_url='/donors/information/')
def interface(request):
    employee = Employee.objects.get(id=request.user.id)
    return render(request, 'employees/interface.html', {'employee': employee})
