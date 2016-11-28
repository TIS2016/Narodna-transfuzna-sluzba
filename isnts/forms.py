from django import forms
from .models import *

class PlainTextWidget(forms.Widget):

    def render(self, name, value, attrs=None):
        return ('<input type="hidden" value="' + str(value) + '" name="' + name + '"/>'
            + str(value) + '. ' + self.choices[int(value)][1])


class CreateNewUser(forms.ModelForm):

    class Meta:
        model = DonorCard
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'gender']


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
