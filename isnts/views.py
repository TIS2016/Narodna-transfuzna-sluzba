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
        registration_form = Register(request.POST if request.POST else None)
        return render(request, 'donors/login.html', {'login_form': login_form, 'registration_form': registration_form})

    if not request.user.is_authenticated():
        if request.method == 'POST':
            if request.POST.get('register_btn'):
                form = Register(request.POST)
                if form.is_valid():
                    user = form.save()
                    user.set_password(user.password)
                    user.save()
                    return render(request, 'donors/login.html', {'form': form})
                else:
                    return render_form()
            elif request.POST.get('login_btn'):
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


def donor_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')


def donor_information(request):
    donor = Donor.objects.get(id=request.user.id)
    return render(request, 'donors/information.html', {'donor': donor})


def blood_extraction_listview(request):
    samples = BloodExtraction.objects.exclude(state=1)
    samples_ready_for_exp = BloodExtraction.objects.filter(state=1)
    return render(request, 'blood_extraction/listview.html', {'samples': samples, 'samples_ready_for_exp': samples_ready_for_exp})


def blood_extraction_detailview(request, blood_extraction_id):
    blood_extraction = get_or_none(BloodExtraction, id=blood_extraction_id)
    if request.method == 'POST':
        form = BloodExtractionForm(request.POST, instance=blood_extraction)
        if form.is_valid():
            form.save()
            return render(request, 'blood_extraction/detailview.html', {'form': form})
    else:
        form = BloodExtractionForm(instance=blood_extraction)
    return render(request, 'blood_extraction/detailview.html', {'form': form})
