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


@login_required(login_url='/login/')
@permission_required('isnts.is_employee', login_url='/donors/information/')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='/login/')
@permission_required('isnts.is_employee', login_url='/nopermission/')
def listview(request):
    donors = Donor.objects.all()
    return render(request, 'donors/listview.html', {'donors': donors})


@login_required(login_url='/login/')
@permission_required('isnts.is_employee', login_url='/nopermission/')
def create_new(request):
    donor_form = CreateDonorForm(request.POST or None)
    perm_address_form = AddressForm(
        request.POST or None, prefix='perm_address_form')
    temp_address_form = AddressForm(
        request.POST or None, prefix='temp_address_form')
    if request.method == 'POST':
        if donor_form.is_valid() and perm_address_form.is_valid() and temp_address_form.is_valid():
            perm_address_form.save()
            temp_address_form.save()
            donor_form.save()
    return render(request, 'donors/create_new.html', {
        'donor_form': donor_form,
        'perm_address': perm_address_form,
        'temp_address': temp_address_form
    })


@login_required(login_url='/login/')
@permission_required('isnts.is_employee', login_url='/nopermission/')
def detailview(request, donor_id):
    donor = get_or_none(DonorCard, id=donor_id)
    if not donor:
        return HttpResponseRedirect('/donors/')
    perm_address = get_or_none(
        Address, id=(donor.id_address_perm.id if donor.id_address_perm else None))
    temp_address = get_or_none(
        Address, id=(donor.id_address_temp.id if donor.id_address_temp else None))
    questionnaires = Questionnaire.objects.filter(id_donor=donor_id)
    blood_extractions = BloodExtraction.objects.filter(id_donor=donor_id)
    donor_form = DonorForm(request.POST or None, instance=donor)
    perm_address_form = AddressForm(
        request.POST or None, instance=perm_address, prefix='perm_address_form')
    temp_address_form = AddressForm(
        request.POST or None, instance=temp_address, prefix='temp_address_form')
    if request.method == 'POST':
        if donor_form.is_valid() and perm_address_form.is_valid() and temp_address_form.is_valid():
            perm_address_form.save()
            temp_address_form.save()
            donor_form.save()
    return render(request, 'donors/detailview.html', {
        'donor_form': donor_form,
        'perm_address': perm_address_form,
        'temp_address': temp_address_form,
        'questionnaires': questionnaires,
        'blood_extractions': blood_extractions,
        'donor': donor
    })


@login_required(login_url='/login/')
def quastionnaire(request, donor_id, questionnaire_id):
    if request.user.has_perm('isnts.is_employee') == False and donor_id != request.user.id:
        return HttpResponseRedirect('/nopermission/')
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
    questionnaire_form = QuestionnaireForm(
        request.POST or None, instance=questionnaire)
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


@login_required(login_url='/login/')
@permission_required('isnts.is_employee', login_url='/nopermission/')
def blood_extraction(request, donor_id, blood_extraction_id):
    donor = get_or_none(Donor, id=donor_id)
    employee = get_or_none(Employee, id=request.user.id)
    if not donor:
        return HttpResponseRedirect('/donors/')
    blood_extraction = get_or_none(BloodExtraction, id=blood_extraction_id)
    blood_extraction_form = BloodExtractionForm(
        request.POST or None, instance=blood_extraction)
    if request.method == 'POST':
        if blood_extraction_form.is_valid():
            blood_extraction_form.save()
            blood_extraction.id_nts = employee.id_nts
    return render(request, 'donors/blood_extraction/detailview.html', {
        'blood_extraction_form': blood_extraction_form,
        'donor': donor
    })


@login_required(login_url='/login/')
@permission_required('isnts.is_donor', login_url='/employees/interface/')
def information(request):
    donor = User.objects.get(id=request.user.id)
    return render(request, 'donors/information.html', {'donor': donor})


def terms_choose_nts(request):
    choose_nts_form = ChooseNTSForm(
        request.POST or request.GET, ntss=NTS.objects.all())
    if request.method == 'GET':
        return render(request, 'donors/terms/choose_nts.html', {'choose_nts_form': choose_nts_form})
    elif request.method == 'POST':
        return HttpResponseRedirect('/donors/terms/' + request.POST['nts'])


def terms_choose_day(request, nts_id=None):
    if nts_id is not None:
        if request.method == 'GET':
            nts = NTS.objects.get(id=nts_id)
            office_hours = OfficeHours.objects.filter(id_nts=nts)
            avail_days = set()
            for oh in office_hours:
                avail_days.add(int(oh.day))
            all_days = set([1, 2, 3, 4, 5, 6, 7])
            not_avail_days = list(all_days - avail_days)
            choose_daytime_form = ChooseDayTimeForm(request.POST or None)
            return render(request, 'donors/terms/choose_day.html', {'choose_daytime_form': choose_daytime_form, 'not_avail_days': not_avail_days})
        else:
            chosen_day = request.POST['day']
            print(chosen_day)
    return HttpResponseRedirect('/')
