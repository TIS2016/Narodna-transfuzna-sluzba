from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.shortcuts import render
from django import forms
from isnts.models import *
from isnts.forms import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import PasswordChangeForm


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
                login(request, user)
                return HttpResponseRedirect('/donors/information')
            else:
                return render_form()
        else:
            return render_form()
    return HttpResponseRedirect('/donors/information/')


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

@login_required(login_url='/login/')
def donor_password_change(request):
    password_change_form = PasswordChangeForm(user=request.user, data=(request.POST or None))
    if request.method == 'POST':
        if password_change_form.is_valid():
            password_change_form.save()
            update_session_auth_hash(request, password_change_form.user)
            return HttpResponseRedirect('/login/')
    return render(request, 'donors/password_change.html', {'form': password_change_form})


def employee_login(request):
    def render_form():
        employee_login_form = EmployeeLogin(request.POST if request.POST else None)
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
    def render_form():
        employee_registration_form = EmployeeRegister(request.POST if request.POST else None)
        return render(request, 'employees/register.html', {'form': employee_registration_form})

    if not request.user.is_authenticated():
        if request.method == 'POST':
            employee_registration_form = EmployeeRegister(request.POST)
            if employee_registration_form.is_valid():
                user = employee_registration_form.save()
                user.set_password(user.password)
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
