from django.shortcuts import render
from django import forms
from .models import Donor
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def error404(request):
    return HttpResponse("404 error")


def home(request):
    return render(request, 'home.html')


def donor_listview(request):
    donors = Donor.objects.all()
    return render(request, 'donors/listview.html', {'donors': donors})


def donor_detail(request, donor_id):
    donor = get_or_none(Donor, id=donor_id)
    if request.method == 'POST':
        form = CreateNewUser(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            return render(request, 'donors/detailview.html', {'form': form})
    else:
        form = CreateNewUser(instance=donor)
    return render(request, 'donors/detailview.html', {'form': form})

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


def donor_information(request):
    donor = Donor.objects.get(id=request.user.id)
    return render(request, 'donors/information.html', {'donor': donor})

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

def employee_listview(request):
    employees = Employee.objects.all()
    return render(request, 'employees/listview.html', {'employees': employees})

def employee_detail(request, employee_id):
    employee = get_or_none(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeRegister(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return render(request, 'employees/detailview.html', {'form': form})
    else:
        form = EmployeeRegister(instance=employee)
    return render(request, 'employees/detailview.html', {'form': form})

def employee_interface(request):
    employee = Employee.objects.get(id=request.user.id)
    return render(request, 'employees/interface.html', {'employee': employee})

def employee_logout(request):
    logout(request)
    return HttpResponseRedirect('/employees/login')
