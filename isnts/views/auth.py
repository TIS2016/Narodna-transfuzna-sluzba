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


def donor_pass_change(request):
    form = PassChange()
    return render(request, 'donors/pass_change.html', {'form': form})

def employee_login(request):
    def render_form():
        form = EmployeeLogin(request.POST if request.POST else None)
        return render(request, 'employees/login.html', {'form': form})

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
        form = EmployeeRegister(request.POST if request.POST else None)
        return render(request, 'employees/register.html', {'form': form})

    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = EmployeeRegister(request.POST)
            if form.is_valid():
                user = form.save()
                user.set_password(user.password)
                user.save()
                return render(request, 'employees/register.html', {'form': form})
            else:
                return render_form()
        else:
            return render_form()
    return HttpResponseRedirect('/donors/information/')


def employee_logout(request):
    logout(request)
    return HttpResponseRedirect('/employees/login')
