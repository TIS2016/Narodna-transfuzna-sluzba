from django.shortcuts import render
from django import forms
from .models import Donor
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def error404(request):
    return HttpResponse("404 error")


def is_not_admin(user):
    return user.is_superuser == False


@login_required(login_url='/login/')
@permission_required('is_employee', login_url='/donors/information/')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='/login/')
@permission_required('is_employee', login_url='/nopermission/')
def donor_listview(request):
    donors = Donor.objects.all()
    return render(request, 'donors/listview.html', {'donors': donors})


def donor_detail(request, donor_id):
    if request.user.id == donor_id or request.user.has_perm('is_employee'):
        donor = get_or_none(Donor, id=donor_id)
    else:
        return HttpResponseRedirect('/nopermission/')
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


@login_required(login_url='/login/')
@user_passes_test(is_not_admin, login_url='/admin/')
def donor_information(request):
    donor = User.objects.get(id=request.user.id)
    return render(request, 'donors/information.html', {'donor': donor})
