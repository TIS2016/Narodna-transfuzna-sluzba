from django.shortcuts import render
from django import forms
from isnts.models import *
from isnts.forms import *
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from isnts.questions_enum import QUESTION_COUNT
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def is_not_admin(user):
    return user.is_superuser == False


@login_required(login_url='/login/')
@permission_required('is_employee', login_url='/donors/information/')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='/login/')
@permission_required('is_employee', login_url='/nopermission/')
def listview(request):
    donors = Donor.objects.all()
    return render(request, 'donors/listview.html', {'donors': donors})


def detailview(request, donor_id):
    if request.user.id == donor_id or request.user.has_perm('is_employee'):
        donor = get_or_none(DonorCard, id=donor_id)
        perm_address = get_or_none(Address, id=donor.id_address_perm.id if donor else None)
        temp_address = get_or_none(Address, id=donor.id_address_temp.id if donor else None)
        questionnaires = Questionnaire.objects.filter(id_donor=donor_id)
        blood_extractions = BloodExtraction.objects.filter(id_donor=donor_id)
    else:
        return HttpResponseRedirect('/nopermission/')
    donor_form = DonorForm(request.POST or None, instance=donor)
    perm_address_form = AddressForm(request.POST or None, instance=perm_address, prefix='perm_address_form')
    temp_address_form = AddressForm(request.POST or None, instance=temp_address, prefix='temp_address_form')
    if request.method == 'POST':
        if donor_form.is_valid() and perm_address_form.is_valid() and temp_address_form.is_valid():
            perm_address_form.save()
            temp_address_form.save()
            if not donor:
                donor_form.instance.id_address_perm = perm_address_form.instance
                donor_form.instance.id_address_temp = temp_address_form.instance
            donor_form.save()
    return render(request, 'donors/detailview.html', {
        'donor_form': donor_form,
        'perm_address': perm_address_form,
        'temp_address': temp_address_form,
        'questionnaires': questionnaires,
        'blood_extractions': blood_extractions,
        'donor': donor
    })


def quastionnaire(request, donor_id, questionnaire_id):
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
    return render(request, 'donors/questionnaire/detailview.html', {
        'donor': donor,
        'questionnaire_form': questionnaire_form,
        'questions_forms': questions_forms
    })


def blood_extraction(request, donor_id, blood_extraction_id):
    donor = get_or_none(Donor, id=donor_id)
    if not donor:
        return HttpResponseRedirect('/donors/')
    blood_extraction = get_or_none(BloodExtraction, id=blood_extraction_id)
    blood_extraction_form = BloodExtractionForm(request.POST or None, instance=blood_extraction)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    return render(request, 'donors/blood_extraction/detailview.html', {
        'blood_extraction_form': blood_extraction_form,
        'donor': donor
    })



@login_required(login_url='/login/')
@user_passes_test(is_not_admin, login_url='/admin/')
def information(request):
    donor = User.objects.get(id=request.user.id)
    return render(request, 'donors/information.html', {'donor': donor})
