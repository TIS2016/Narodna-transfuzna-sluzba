from django import forms
from .models import *
from datetime import time


class PlainTextWidget(forms.Widget):

    def render(self, name, value, attrs=None):
        return ('<input type="hidden" value="' + str(value) + '" name="' + name + '"/>'
                + str(value) + '. ' + self.choices[int(value)][1])


class DonorForm(forms.ModelForm):
    field_order = ['active_acount']
    class Meta:
        model = DonorCard
        exclude = ['password', 'card_created_by', 'id_address_perm', 'id_address_temp',
                   'last_login', 'is_superuser', 'email_verification_token', 'name', 'is_staff',
                   'groups', 'user_permissions', 'is_active', 'email', 'date_joined', 'username']
        widgets = {
            'can_donate_from': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date', 'id': 'datepicker'})
        }


class CreateDonorForm(forms.ModelForm):

    class Meta:
        model = DonorCard
        exclude = ['password', 'card_created_by', 'id_address_perm', 'id_address_temp',
                   'last_login', 'is_superuser', 'email_verification_token', 'name', 'is_staff',
                   'groups', 'user_permissions', 'is_active', 'active_acount', 'date_joined', 'username']
        widgets = {
            'can_donate_from': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date', 'id': 'datepicker'})
        }

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = '__all__'


class BloodExtractionForm(forms.ModelForm):

    class Meta:
        model = BloodExtraction
        exclude = ['id_nts', 'date', 'id_donor']


class Login(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class Register(forms.ModelForm):

    class Meta:
        model = DonorCard
        fields = ['first_name', 'last_name',
                  'username', 'email', 'password', 'gender']
        widgets = {
            'password': forms.PasswordInput()
        }


class EmployeeRegister(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        k = kwargs.pop('emp_types', [])
        super(EmployeeRegister, self).__init__(*args, **kwargs)
        self.fields['employee_type'] = forms.TypedChoiceField(
            choices=k, coerce=int, required=True)

    secret_key = forms.CharField(required=True)

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class EmployeeLogin(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class QuestionnaireForm(forms.ModelForm):

    class Meta:
        model = Questionnaire
        fields = ['weight', 'height']
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
        self.fields['time'] = TimeModelChoiceField(choices=times, coerce=time,
                                                   required=True)

    class Meta:
        model = Booking
        fields = []


class SecretKeyChange(forms.Form):

    secret_key_new = forms.CharField(
        label='New secret key', max_length=30, required=True)
    secret_key_new2 = forms.CharField(
        label='New secret key', max_length=30, required=True)


class EmployeeActivationForm(forms.Form):

    activate = forms.BooleanField()


class OfficeHoursForm(forms.ModelForm):

    class Meta:
        model = OfficeHours
        fields = ['open_time', 'close_time']

    def __init__(self, *args, **kwargs):
        super(OfficeHoursForm, self).__init__(*args, **kwargs)
        self.fields['open_time'].required = False
        self.fields['close_time'].required = False
        self.fields['open_time'].input_format = "%H:%M"
        self.fields['close_time'].input_format = "%H:%M"
        self.fields['open_time'].widget = forms.TimeInput(format="%H:%M")
        self.fields['close_time'].widget = forms.TimeInput(format="%H:%M")

    def is_valid(self):
        for field in self.fields:
            if 'open_time' in field:
                ot = field
            elif 'close_time' in field:
                ct = field
        is_good = True

        if self.data[ot] != '' and self.data[ct] != '':
            k = self.data[ot].split(':')
            open_time = time(int(k[0]), int(k[1]))
            k = self.data[ct].split(':')
            close_time = time(int(k[0]), int(k[1]))
            is_good = open_time < close_time
            if is_good == False:
                self.errors[' open time: '] = self.data[ot]
                self.errors[' close time: '] = self.data[ct]
        return is_good and super(OfficeHoursForm, self).is_valid()
