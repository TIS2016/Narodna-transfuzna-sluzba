from django.shortcuts import render
from django import forms


def home(request):
    class NameForm(forms.Form):
        your_name = forms.CharField(label='Your name', max_length=100)
    return render(request, 'home.html', {"form": NameForm()})
