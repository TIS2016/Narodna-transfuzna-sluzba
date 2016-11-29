from isnts.models import *
from isnts.forms import *
from django.shortcuts import render



def listview(request):
    employees = Employee.objects.all()
    return render(request, 'employees/listview.html', {'employees': employees})


def detailview(request, employee_id):
    employee = get_or_none(Employee, id=employee_id)
    if request.method == 'POST':
        employee_form = EmployeeRegister(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return render(request, 'employees/detailview.html', {'form': employee_form})
    else:
        employee_form = EmployeeRegister(instance=employee)
    return render(request, 'employees/detailview.html', {'form': employee_form})


def interface(request):
    employee = Employee.objects.get(id=request.user.id)
    return render(request, 'employees/interface.html', {'employee': employee})
