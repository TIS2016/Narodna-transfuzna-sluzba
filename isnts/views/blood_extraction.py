from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.shortcuts import render
from isnts.models import *
from isnts.forms import *


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None

@login_required(login_url='/login/')
@permission_required('isnts.is_employee',login_url='/nopermission/')
def listview(request):
    samples_new = BloodExtraction.objects.filter(state=0)
    samples_ready_for_exp = BloodExtraction.objects.filter(state=1)
    samples_shipped = BloodExtraction.objects.filter(state=2)
    return render(request, 'blood_extraction/listview.html', {
        'samples_new': samples_new,
        'samples_ready_for_exp': samples_ready_for_exp,
        'samples_shipped': samples_shipped
    })

@login_required(login_url='/login/')
@permission_required('isnts.is_employee',login_url='/nopermission/')
def detailview(request, blood_extraction_id):
    blood_extraction = get_or_none(BloodExtraction, id=blood_extraction_id)
    blood_extraction_form = BloodExtractionForm(request.POST or None, instance=blood_extraction)
    if request.method == 'POST':
        if blood_extraction_form.is_valid():
            blood_extraction_form.save()
    return render(request, 'blood_extraction/detailview.html', {'blood_extraction_form': blood_extraction_form})
