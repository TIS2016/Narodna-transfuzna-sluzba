from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.shortcuts import render
from django import forms
from isnts.models import *
from isnts.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied


def error404(request):
    return HttpResponse("404 error")


def permission_denied(request):
    raise PermissionDenied


def donor_login(request):
    def render_form():
        login_form = Login(request.POST if request.POST else None)
        return render(request, 'donors/login.html', {'login_form': login_form})

    if not request.user.is_authenticated():
        if request.method == 'POST':
            user = authenticate(username=request.POST.get('username'),
                                password=request.POST.get('password'))
            if user is not None:
                if user.has_perm('isnts.is_donor') == False:
                    return HttpResponseRedirect('/login')
                login(request, user)
                return HttpResponseRedirect('/donors/information')
            else:
                return render_form()
    else:
        user = User.objects.get(id=request.user.id)
        if user.has_perm('isnts.is_donor'):
            return HttpResponseRedirect('/donors/information/')
        elif user.has_perm('isnts.is_employee'):
            return HttpResponseRedirect('/')
        return render_form()
    return render_form()


def donor_register(request):
    def render_form():
        registration_form = Register(request.POST if request.POST else None)
        return render(request, 'donors/register.html', {'registration_form': registration_form})

    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = Register(request.POST)
            if form.is_valid():
                user = form.save()
                user.set_password(user.password)
                g = Group.objects.get(name='Donor')
                g.user_set.add(user)
                user.save()
                return render(request, 'donors/register.html', {'form': form})
            else:
                return render_form()
        else:
            return render_form()
    return HttpResponseRedirect('/donors/information/')


def donor_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')


def donor_pass_change(request):
    form = PassChange()
    return render(request, 'donors/pass_change.html', {'form': form})


def employee_login(request):
    def render_form():
        employee_login_form = EmployeeLogin(
            request.POST if request.POST else None)
        return render(request, 'employees/login.html', {'form': employee_login_form})

    if not request.user.is_authenticated():
        if request.method == 'POST':
            user = authenticate(username=request.POST.get('username'),
                                password=request.POST.get('password'))
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/employees/interface')
            else:
                return render_form()
        else:
            return render_form()
    return HttpResponseRedirect('/employees/interface/')


def employee_register(request):
    e_types = [('', '---------')]
    e_types += list((int(g.id), g.name)
                    for g in Group.objects.exclude(name='NTSsu').exclude(name='Donor'))

    def render_form():
        employee_registration_form = EmployeeRegister(
            request.POST if request.POST else None,emp_types=e_types)
        return render(request, 'employees/register.html', {'form': employee_registration_form})

    if not request.user.is_authenticated():
        if request.method == 'POST':
            employee_registration_form = EmployeeRegister(
                request.POST, emp_types=e_types)

            if employee_registration_form.is_valid():
                user = employee_registration_form.save()
                user.set_password(user.password)
                g = Group.objects.get(
                    id=employee_registration_form.cleaned_data['employee_type'])
                g.user_set.add(user)
                user.save()
                return render(request, 'employees/register_message.html', {'form': employee_registration_form})
            else:
                return render_form()
        else:
            return render_form()
    return HttpResponseRedirect('/')


def employee_logout(request):
    logout(request)
    return HttpResponseRedirect('/employees/login')
