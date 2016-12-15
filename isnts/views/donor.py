from datetime import datetime, timedelta

from django import forms
from django.contrib.auth.decorators import (login_required,
                                            permission_required,
                                            user_passes_test)
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from isnts.forms import *
from isnts.models import *
from isnts.questions_enum import QUESTION_COUNT
from django.core import serializers
from django.db.models import Max


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
    if blood_extraction is None:
        blood_extraction = BloodExtraction()
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


@login_required(login_url="/login/")
@permission_required("isnts.is_donor", login_url="/employees/interface/")
def terms_choose_nts(request, no_office_hours=None):
    choose_nts_form = ChooseNTSForm(
        request.POST or request.GET, ntss=NTS.objects.all())
    if request.method == 'GET':
        if no_office_hours is not None:
            return render(request, 'donors/terms/choose_nts.html', {'choose_nts_form': choose_nts_form, 'no_office_hours': no_office_hours})
        else:
            return render(request, 'donors/terms/choose_nts.html', {'choose_nts_form': choose_nts_form})
    elif request.method == 'POST':
        return HttpResponseRedirect('/donors/terms/' + request.POST['nts'])


def generate_times(open_time, close_time):
    res = []
    fifteen_minutes = timedelta(minutes=15)
    time = datetime(2000, 1, 1, open_time.hour, open_time.minute)
    end_time = datetime(2000, 1, 1, close_time.hour, close_time.minute)
    while time <= end_time:
        res.append((time.time(), time.time().strftime("%H:%M")))
        time += fifteen_minutes
    return res


@login_required(login_url="/login/")
@permission_required("isnts.is_donor", login_url="/employees/interface/")
def terms_choose_day(request, nts_id=None):
    donor = Donor.objects.get(id=request.user.id)
    if nts_id is not None:
        nts = NTS.objects.get(id=nts_id)
        if request.method == 'GET':
            office_hours = OfficeHours.objects.filter(id_nts=nts)
            create_booking_form = CreateBookingForm(None)
            if office_hours.exists() is False:
                return terms_choose_nts(request, no_office_hours=nts)
            avail_days = set()
            for oh in office_hours:
                avail_days.add(int(oh.day))
            all_days = set([1, 2, 3, 4, 5, 6, 7])
            not_avail_days = list(all_days - avail_days)

            if request.GET.get('datepicked'):
                picked_date = request.GET.get('datepicked')
                date = picked_date.split('.')
                date = datetime(int(date[2]), int(date[1]), int(date[0]))
                day = date.isoweekday()
                times = set()
                for d in office_hours:
                    if d.day == day:
                        t = generate_times(d.open_time, d.close_time)
                        for x in t:
                            times.add(x)
                times = sorted(list(times))
                create_booking_form = CreateBookingForm(
                    request.POST or None, times=list(times))
                create_booking_form.fields['day'].initial = picked_date
            most_recent_date = BloodExtraction.objects.filter(id_donor=donor).aggregate(Max('date'))['date__max']
            most_recent_blood_extraction = get_or_none(BloodExtraction, date=most_recent_date)
            if most_recent_blood_extraction is not None:
                postpone = most_recent_blood_extraction.postpone
            else:
                postpone = None
            return render(request, 'donors/terms/create_booking.html', {'create_booking_form': create_booking_form, 'not_avail_days': not_avail_days, 'postpone': postpone})
        else:
            if 'day' not in request.POST.keys():
                return terms_choose_nts(request, no_office_hours=nts)
            chosen_day = request.POST['day']
            day = chosen_day.split('.')
            time = request.POST['time']
            time = time.split(':')
            dt = datetime(int(day[2]), int(day[1]), int(
                day[0]), int(time[0])+1, int(time[1]))
            booking = Booking(id_nts=nts, id_donor=donor, booking_time=dt)
            booking.save()

    return HttpResponseRedirect('/donors/terms/list')


@login_required(login_url="/login/")
@permission_required("isnts.is_donor", login_url="/employees/interface/")
def terms_listview(request):
    donor = Donor.objects.get(id=request.user.id)
    now = timezone.now()
    future_bookings = Booking.objects.all().filter(
        id_donor=donor).filter(booking_time__gte=now)
    for e in future_bookings:
        e.booking_time = e.booking_time.strftime("%d.%m.%Y %H:%M")
    return render(request, 'donors/terms/listview.html', {'bookings': future_bookings})


class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = data
        kwargs["content_type"] = "application/json"
        super(JSONResponse, self).__init__(content, **kwargs)


@login_required(login_url="/login/")
@permission_required("isnts.is_donor", login_url="/employees/interface/")
def terms_remove(request, booking_id):
    donor = Donor.objects.get(id=request.user.id)
    booking = Booking.objects.get(id=booking_id)
    now = timezone.now()
    deleted_booking = Booking.objects.filter(
        id=booking_id).values("id", "booking_time", "id_nts__name")
    data = []
    for d in deleted_booking:
        d["booking_time"] = d["booking_time"].strftime("%d.%m.%Y %H:%M")
        data.append(d)
    data = str(data)
    data = data.replace("\'", '\"')
    if now <= booking.booking_time:
        booking.delete()
    return JSONResponse(data)
