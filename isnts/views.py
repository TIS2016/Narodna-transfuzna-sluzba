from django.shortcuts import render
from django import forms
from .models import Donor
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login


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
    if not request.user.is_authenticated():
        if request.method == 'POST':
            if request.POST.get('register_btn'):
                form = Register(request.POST)
                if form.is_valid():
                    form.save()
                    return render(request, 'donors/login.html', {'form': form})
            elif request.POST.get('login_btn'):
                print(request.POST.get('username'))
                print(request.POST.get('password'))
                user = authenticate(username=request.POST.get('username'),
                                    password=request.POST.get('password'))
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/donors/information/')
                else:
                    return HttpResponseRedirect('/donors/not')
        else:
            form1 = Login()
            form2 = Register()
            return render(request, 'donors/login.html', {'form1': form1, 'form2': form2})
    return HttpResponseRedirect('/donors/information/')
