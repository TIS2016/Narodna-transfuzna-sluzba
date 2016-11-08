from django.shortcuts import render
from django import forms


def home(request):
    return render(request, 'donor_login.html')
