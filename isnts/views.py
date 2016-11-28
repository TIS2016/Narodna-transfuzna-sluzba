from django.shortcuts import render
from django import forms
from .models import *
from .forms import *
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .questions_enum import QUESTION_COUNT
from django.forms import formset_factory
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required



def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def error404(request):
    return HttpResponse("404 error")

def permission_denied(request):
    raise PermissionDenied

def is_not_admin(user):
    return user.is_superuser == False


@login_required(login_url='/login/')
@permission_required('is_employee', login_url='/donors/information/')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='/login/')
@permission_required('is_employee', login_url='/nopermission/')
def donor_listview(request):
    donors = Donor.objects.all()
    return render(request, 'donors/listview.html', {'donors': donors})


def donor_detail(request, donor_id):
    if request.user.id == donor_id or request.user.has_perm('is_employee'):
        donor = get_or_none(Donor, id=donor_id)
    else:
        return HttpResponseRedirect('/nopermission/')
    form = CreateNewUser(request.POST or None, instance=donor)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    return render(request, 'donors/detailview.html', {'form': form})


def donor_quastionnare(request, donor_id, questionnaire_id):
    donor = get_or_none(Donor, id=donor_id)
    if not donor:
        return HttpResponseRedirect('/donors/')
    questionnaire = get_or_none(Questionnaire, id=questionnaire_id)
    if questionnaire:
        questions = Questions.objects.filter(
            questionnaire_id=questionnaire.id).values('id', 'question', 'answer')
    else:
        questions = list({'question': x} for x in range(1, QUESTION_COUNT + 1))
    QuestionsFormSet = formset_factory(QuestionsForm, extra=0)
    questionnaire_form = QuestionnaireForm(request.POST or None, instance=questionnaire)
    questions_forms = QuestionsFormSet(request.POST or None, initial=questions)
    if request.method == 'POST':
        if questions_forms.is_valid() and questionnaire_form.is_valid():
            questionnaire_form.id_donor = donor_id
            questionnaire_form.save()
            if questionnaire:
                for questions_form in questions_forms:
                    cleaned_data = questions_form.cleaned_data
                    Questions.objects.filter(
                        questionnaire_id=questionnaire.id).filter(
                        question=cleaned_data.get('question')).update(
                        answer=cleaned_data.get('answer')
                    )
            else:
                for questions_form in questions_forms:
                    questions_form.instance.questionnaire = questionnaire_form.instance
                    questions_form.save()
    return render(request, 'donors/questionnaire.html', {
        'donor_id': donor_id,
        'questionnaire_form': questionnaire_form,
        'questions_forms': questions_forms
    })


def donor_login(request):
    def render_form():
        login_form = Login(request.POST if request.POST else None)
        return render(request, 'donors/login.html', {'login_form': login_form})

    if not request.user.is_authenticated():
        if request.method == 'POST':
            user = authenticate(username=request.POST.get('username'),
                                password=request.POST.get('password'))
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/donors/information')
            else:
                return render_form()
        else:
            return render_form()
    return HttpResponseRedirect('/donors/information/')


def donor_register(request):
    def render_form():
        registration_form = Register(request.POST if request.POST else None)
        return render(request, 'donors/register.html', {'registration_form': registration_form})

    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = Register(request.POST)
            if form.is_valid():
                user = form.save()
                user.set_password(user.password)
                g = Group.objects.get(name='Donor')
                g.user_set.add(user)
                user.save()
                return render(request, 'donors/register.html', {'form': form})
            else:
                return render_form()
        else:
            return render_form()
    return HttpResponseRedirect('/donors/information/')


def donor_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')


def donor_pass_change(request):
    form = PassChange()
    return render(request, 'donors/pass_change.html', {'form': form})


@login_required(login_url='/login/')
@user_passes_test(is_not_admin, login_url='/admin/')
def donor_information(request):
    donor = User.objects.get(id=request.user.id)
    return render(request, 'donors/information.html', {'donor': donor})


def blood_extraction_listview(request):
    samples_new = BloodExtraction.objects.filter(state=0)
    samples_ready_for_exp = BloodExtraction.objects.filter(state=1)
    samples_shipped = BloodExtraction.objects.filter(state=2)
    return render(request, 'blood_extraction/listview.html', {'samples_new': samples_new, 'samples_ready_for_exp': samples_ready_for_exp, 'samples_shipped': samples_shipped})


def blood_extraction_detailview(request, blood_extraction_id):
    blood_extraction = get_or_none(BloodExtraction, id=blood_extraction_id)
    form = BloodExtractionForm(request.POST or None, instance=blood_extraction)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    return render(request, 'blood_extraction/detailview.html', {'form': form})
