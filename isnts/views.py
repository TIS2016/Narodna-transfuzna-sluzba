from django.shortcuts import render
from django import forms
from .models import Donor
from .forms import CreateNewUser


def home(request):
    class NameForm(forms.Form):
        your_name = forms.CharField(label='Your name', max_length=100)
    return render(request, 'home.html', {"form": NameForm()})


def donor_listview(request):
    donors = Donor.objects.all()
    return render(request, 'listview.html', {'donors': donors})


def donor_detail(request):
    if request.method == 'POST':
        pass
    else:
        form = CreateNewUser()
    return render(request, 'donor_detail.html', {'form': form})
