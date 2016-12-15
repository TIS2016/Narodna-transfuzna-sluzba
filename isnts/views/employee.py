from isnts.models import *
from isnts.forms import *
from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import time
from django.http import HttpResponseRedirect


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


@login_required(login_url='/employees/login/')
@permission_required('isnts.is_employee', login_url='/nopermission/')
def listview(request):
    employees = Employee.objects.filter(groups__name__in=['Doctor', 'Nurse'])
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


@login_required(login_url='/employees/login/')
@permission_required('isnts.is_employee', login_url='/donors/information/')
def terms_list(request):
    employee = Employee.objects.get(id=request.user.id)
    bookings = Booking.objects.filter(id_nts=employee.id_nts)
    for b in bookings:
        b.booking_time = b.booking_time.strftime("%d.%m.%Y %H:%M")
    return render(request, 'employees/terms/listview.html', {'bookings': bookings})


def check_office_hours(office_hours=[], oh_bn=None, oh_an=None, day=None, id_nts=None):
    if oh_bn.exists() == False:
        if oh_an.exists() == False:
            oh = OfficeHours(day=day, id_nts=id_nts)
            office_hours.append(oh)
            oh = OfficeHours(day=day, id_nts=id_nts)
            office_hours.append(oh)
        elif len(oh_an) == 1:
            oh = OfficeHours(day=day, id_nts=id_nts)
            office_hours.append(oh)
            oh = list(oh_an)[0]
            office_hours.append(oh)
        else:
            oh = list(oh_an)[0]
            office_hours.append(oh)
            oh = list(oh_an)[1]
            office_hours.append(oh)
            for i in range(2, len(oh_an)):
                list(oh_an)[i].delete()
    elif len(oh_bn) == 1:
        if oh_an.exists() == False:
            oh = list(oh_bn)[0]
            office_hours.append(oh)
            oh = OfficeHours(day=day, id_nts=id_nts)
            office_hours.append(oh)
        elif len(oh_an) == 1:
            oh = list(oh_bn)[0]
            office_hours.append(oh)
            oh = list(oh_an)[0]
            office_hours.append(oh)
        else:
            oh = list(oh_bn)[0]
            office_hours.append(oh)
            oh = list(oh_an)[0]
            office_hours.append(oh)
            for i in range(1, len(oh_an)):
                list(oh_an)[i].delete()
    else:
        if oh_an.exists() == False:
            oh = list(oh_bn)[0]
            office_hours.append(oh)
            oh = list(oh_bn)[1]
            office_hours.append(oh)
            for i in range(2, len(oh_bn)):
                list(oh_bn)[i].delete()
        elif len(oh_an) == 1:
            oh = list(oh_bn)[0]
            office_hours.append(oh)
            oh = list(oh_bn)[0]
            office_hours.append(oh)
            for i in range(1, len(oh_an)):
                list(oh_an)[i].delete()
        else:
            oh = list(oh_bn)[0]
            office_hours.append(oh)
            oh = list(oh_an)[0]
            office_hours.append(oh)
            for i in range(1, len(oh_an)):
                list(oh_an)[i].delete()
            for i in range(1, len(oh_bn)):
                list(oh_bn)[i].delete()
    return office_hours

@login_required(login_url='/employees/login/')
@permission_required('isnts.is_employee', login_url='/donors/information/')
def office_hours(request):
    employee = Employee.objects.get(id=request.user.id)
    oh = OfficeHours.objects.filter(id_nts=employee.id_nts)
    noon = time(12, 0)
    days_in_week = ['Monday', 'Tuesday', 'Wednesday',
                    'Thursday', 'Friday', 'Saturday', 'Sunday']
    forms = {}
    office_hours = []
    for day in range(1, 8):
        oh_bn = OfficeHours.objects.filter(id_nts=employee.id_nts, day=day, close_time__lte=noon)
        oh_an = OfficeHours.objects.filter(id_nts=employee.id_nts, day=day, close_time__gt=noon)
        office_hours = check_office_hours(office_hours=office_hours, oh_bn=oh_bn, oh_an=oh_an, day=day, id_nts=employee.id_nts)
        
    for i in range(len(office_hours)):
        p = forms.get(i // 2, [])
        form = OfficeHoursForm(request.POST or None, instance=office_hours[i])
        form.fields['open_time'].initial = office_hours[i].open_time
        form.fields['close_time'].initial = office_hours[i].close_time
        form.fields['open_time' + str(i)] = form.fields['open_time']
        del form.fields['open_time']
        form.fields['close_time' + str(i)] = form.fields['close_time']
        del form.fields['close_time']
        p.append(form)
        forms[i // 2] = p
    if request.method == 'GET':
        return render(request, 'employees/officehours.html', {'forms': forms, 'days_in_week': days_in_week})
    j = 0
    i = 0
    for oh in office_hours:
        form = forms[i][j]
        k = (i * 2) + j
        if j % 2 == 1:
            i += 1
        j += 1
        j = j % 2

        if form.is_valid():
            cleaned_data = form.clean()
            if cleaned_data['open_time' + str(k)] is None or cleaned_data['close_time' + str(k)] is None:
                if office_hours[k].id is not None:
                    office_hours[k].delete()
                continue
            ot = [cleaned_data['open_time' +
                               str(k)].hour, cleaned_data['open_time' + str(k)].minute]
            ct = [cleaned_data['close_time' +
                               str(k)].hour, cleaned_data['close_time' + str(k)].minute]
            office_hours[k].open_time = time(int(ot[0]), int(ot[1]))
            office_hours[k].close_time = time(int(ct[0]), int(ct[1]))
            office_hours[k].save()
        else:
            print(form.errors)
            return render(request, 'employees/officehours.html', {'forms': forms, 'days_in_week': days_in_week, 'bad_time_input': form.errors})

    return render(request, 'employees/officehours.html', {'forms': forms, 'days_in_week': days_in_week})
