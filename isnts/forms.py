from django import forms
from .models import *
from datetime import time


class PlainTextWidget(forms.Widget):

    def render(self, name, value, attrs=None):
        return ('<input type="hidden" value="' + str(value) + '" name="' + name + '"/>'
                + str(value) + '. ' + self.choices[int(value)][1])


class DonorForm(forms.ModelForm):

    class Meta:
        model = DonorCard
        exclude = ['password', 'card_created_by', 'id_address_perm', 'id_address_temp',
                   'last_login', 'is_superuser', 'email_verification_token', 'name', 'is_staff',
                   'groups', 'user_permissions', 'is_active', 'active_acount', 'email']


class CreateDonorForm(forms.ModelForm):

    class Meta:
        model = DonorCard
        exclude = ['password', 'card_created_by', 'id_address_perm', 'id_address_temp',
                   'last_login', 'is_superuser', 'email_verification_token', 'name', 'is_staff',
                   'groups', 'user_permissions', 'is_active', 'active_acount']


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
        fields = ['first_name', 'last_name',
                  'username', 'email', 'password', 'gender']


class EmployeeRegister(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        k = kwargs.pop('emp_types', [])
        super(EmployeeRegister, self).__init__(*args, **kwargs)
        self.fields['employee_type'] = forms.TypedChoiceField(
            choices=k, coerce=int, required=True)

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


class NTSModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.name


class ChooseNTSForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        ntss = kwargs.pop('ntss', [])
        super(ChooseNTSForm, self).__init__(*args, **kwargs)
        self.fields['nts'] = NTSModelChoiceField(
            queryset=ntss, empty_label="--------", required=True)

    class Meta:
        model = NTS
        fields = []


class ChooseDayTimeForm(forms.ModelForm):

    day = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'datepicker', 'type': 'date', 'id': 'datepicker'}))

    class Meta:
        model = OfficeHours
        fields = []


class TimeModelChoiceField(forms.TypedChoiceField):

    def label_from_instance(self, obj):
        return obj.isoformat()


class CreateBookingForm(forms.ModelForm):

    day = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'datepicker', 'type': 'date'}))

    def __init__(self, *args, **kwargs):
        times = kwargs.pop('times', [])
        super(CreateBookingForm, self).__init__(*args, **kwargs)
        self.fields['time'] = TimeModelChoiceField(choices=times,coerce=time,
                                                   required=True)

    class Meta:
        model = Booking
        fields = []
