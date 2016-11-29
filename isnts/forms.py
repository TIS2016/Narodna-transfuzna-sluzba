from django import forms
from .models import *


class PlainTextWidget(forms.Widget):

    def render(self, name, value, attrs=None):
        return ('<input type="hidden" value="' + str(value) + '" name="' + name + '"/>'
                + str(value) + '. ' + self.choices[int(value)][1])


class DonorForm(forms.ModelForm):

    class Meta:
        model = DonorCard
        exclude = ['password', 'card_created_by', 'id_address_perm', 'id_address_temp',
                   'last_login', 'is_superuser', 'email_verification_token', 'name', 'is_staff',
                   'groups', 'user_permissions', 'active', 'active_acount']


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = '__all__'


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


class QuestionnaireForm(forms.ModelForm):

    class Meta:
        model = Questionnaire
        fields = ['weight', 'height', 'id_donor']
        widget = {
            'id_donor': forms.HiddenInput()
        }


class QuestionsForm(forms.ModelForm):

    class Meta:
        model = Questions
        fields = ['question', 'answer']
        widgets = {
            'question': PlainTextWidget(),
        }


class PassChange(forms.Form):
    old_password = forms.CharField()
    new_password = forms.CharField()
    new_password2 = forms.CharField()
