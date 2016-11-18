from django import forms
from .models import *


class CreateNewUser(forms.ModelForm):

    class Meta:
        model = DonorCard
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'gender']

class Login(forms.ModelForm):

    class Meta:
        model = Donor
        fields = ['username', 'password']

class Register(forms.ModelForm):

    class Meta:
        model = DonorCard
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'gender']
