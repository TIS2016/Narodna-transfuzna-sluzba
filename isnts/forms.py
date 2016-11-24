from django import forms
from .models import *


class CreateNewUser(forms.ModelForm):

    class Meta:
        model = DonorCard
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'gender']


class BloodExtractionForm(forms.ModelForm):

    class Meta:
        model = BloodExtraction
        exclude = ['id_nts', 'blood_type']


class Login(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']


class Register(forms.ModelForm):

    class Meta:
        model = DonorCard
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'gender']
