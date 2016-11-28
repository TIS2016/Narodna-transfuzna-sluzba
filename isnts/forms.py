from django import forms
from .models import *


class CreateNewUser(forms.ModelForm):

    class Meta:
        model = DonorCard
        fields = ['first_name', 'last_name',
                  'username', 'email', 'password', 'gender']


class BloodExtractionForm(forms.ModelForm):

    class Meta:
        model = BloodExtraction
        exclude = ['id_nts']

class Login(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']


class Register(forms.ModelForm):

    class Meta:
        model = DonorCard
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'gender']

class EmployeeRegister(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

class EmployeeLogin(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['username', 'password']

class PassChange(forms.Form):
    old_password = forms.CharField()
    new_password = forms.CharField()
    new_password2 = forms.CharField()
