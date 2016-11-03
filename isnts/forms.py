from django import forms
from .models import Donor


class CreateNewUser(forms.ModelForm):

    class Meta:
        model = Donor
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password': forms.PasswordInput(),
        }
