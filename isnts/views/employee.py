from isnts.models import *
from isnts.forms import *
from django.shortcuts import render
from django.contrib.auth.models import Group


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def listview(request):
    employees = Employee.objects.all()
    return render(request, 'employees/listview.html', {'employees': employees})


def detailview(request, employee_id):
    e_types = [('', '---------')]
    e_types += list((int(g.id), g.name)
                    for g in Group.objects.exclude(name='NTSsu').exclude(name='Donor'))
    employee = get_or_none(Employee, id=employee_id)
    if request.method == 'POST':
        employee_form = EmployeeRegister(request.POST, instance=employee, emp_types=e_types)
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


def interface(request):
    employee = Employee.objects.get(id=request.user.id)
    return render(request, 'employees/interface.html', {'employee': employee})
