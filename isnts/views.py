from django.shortcuts import render
from django import forms
from .models import Donor
from .forms import CreateNewUser


def home(request):
    return render(request, 'home.html')
