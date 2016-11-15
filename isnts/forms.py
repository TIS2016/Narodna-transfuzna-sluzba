from django import forms
from .models import Donor


class CreateNewUser(forms.ModelForm):

    class Meta:
        model = Donor
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'gender']
