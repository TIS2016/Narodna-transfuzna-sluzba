from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.shortcuts import render
from django import forms, http
from isnts.models import *
from isnts.forms import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import EmailMultiAlternatives



def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def error404(request):
    return HttpResponse("404 error")


def permission_denied(request):
    raise PermissionDenied


def donor_login(request):
    def render_form():
        login_form = Login(request.POST if request.POST else None)
        return render(request, 'donors/login.html', {'login_form': login_form})

    if not request.user.is_authenticated():
        if request.method == 'POST':
            user = authenticate(username=request.POST.get('username'),
                                password=request.POST.get('password'))
            if user is not None:
                if user.has_perm('isnts.is_donor') == False:
                    return HttpResponseRedirect('/login')
                login(request, user)
                return HttpResponseRedirect('/donors/information')
            else:
                return render_form()
    else:
        user = User.objects.get(id=request.user.id)
        if user.has_perm('isnts.is_donor'):
            return HttpResponseRedirect('/donors/information/')
        elif user.has_perm('isnts.is_employee'):
            return HttpResponseRedirect('/')
        return render_form()
    return render_form()


def donor_registration(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/donors/information/')
    registration_form = Register(request.POST or None)
    if request.method == 'POST':
        if registration_form.is_valid():
            user = registration_form.save()
            user.set_password(user.password)
            user.is_active = False
            g = Group.objects.get(name='Donor')
            g.user_set.add(user)
            user.save()

            token = default_token_generator.make_token(user)
            context = Context({
                'first_name': user.first_name,
                'last_name': user.last_name,
                'protocol': request.scheme,
                'domain': request.get_host,
                'donor_id': user.id,
                'token': token
            })
            subject = 'Verification'
            text_content = get_template('emails/verification.txt').render(context)
            html_content = get_template('emails/verification.html').render(context)
            message = EmailMultiAlternatives(subject, text_content,'ntssrdebug@gmail.com', [user.email])
            message.attach_alternative(html_content, "text/html")

            try:
                message.send()
            except:
                return HttpResponseRedirect("/registration/send_email_error")
            return HttpResponseRedirect("/registration/success")
    return render(request, 'donors/registration.html', {'registration_form': registration_form})

def donor_registration_confirm(request, donor_id, token):
    if donor_id is not None and token is not None:
        validlink = False
        try:
            user_model = get_user_model()
            user = user_model.objects.get(pk=donor_id)
            if default_token_generator.check_token(user, token) and (not user.is_active):
                validlink = True
                user.is_active = True
                user.save()
        except:
            pass
    return render(request, "donors/registration_confirm.html", {'validlink': validlink})

def donor_registration_success(request):
    return render(request, 'donors/registration_success.html')

# Views below is defined for Donors and Employees


def _password_reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='auth/password_reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect='/login')


def _password_reset(request):
    return password_reset(request, template_name='auth/password_reset_form.html',
        email_template_name='emails/password_reset.txt',
        html_email_template_name='emails/password_reset.html',
        subject_template_name='emails/password_reset_subject.txt',
        post_reset_redirect='/password_reset_sent')


def password_reset_sent(request):
    return render(request, 'auth/password_reset_sent.html')

@login_required(login_url='/login/')
def password_change(request):
    password_change_form = PasswordChangeForm(
        user=request.user, data=(request.POST or None))
    if request.method == 'POST':
        if password_change_form.is_valid():
            password_change_form.save()
            update_session_auth_hash(request, password_change_form.user)
            return HttpResponseRedirect('/login/')
    return render(request, 'auth/password_change.html', {'form': password_change_form})


def employee_login(request):
    def render_form():
        employee_login_form = EmployeeLogin(
            request.POST if request.POST else None)
        return render(request, 'employees/login.html', {'form': employee_login_form})

    if not request.user.is_authenticated():
        if request.method == 'POST':
            user = authenticate(username=request.POST.get('username'),
                                password=request.POST.get('password'))
            if user is not None:
                if user.has_perm('isnts.is_employee') == False:
                    return HttpResponseRedirect('/employees/login/')
                login(request, user)
                return HttpResponseRedirect('/employees/interface')
            else:
                return render_form()
        else:
            return render_form()
    return HttpResponseRedirect('/employees/interface/')


def employee_register(request):
    e_types = [('', '---------')]
    e_types += list((int(g.id), g.name)
                    for g in Group.objects.exclude(name='NTSsu').exclude(name='Donor'))

    def render_form():
        employee_registration_form = EmployeeRegister(
            request.POST if request.POST else None, emp_types=e_types)
        return render(request, 'employees/register.html', {'form': employee_registration_form})

    if not request.user.is_authenticated():
        if request.method == 'POST':
            employee_registration_form = EmployeeRegister(
                request.POST, emp_types=e_types)

            if employee_registration_form.is_valid():
                data = employee_registration_form.cleaned_data
                employee_secret_key = data['secret_key']
                user = employee_registration_form.save()
                user.set_password(user.password)
                user.is_active = False
                g = Group.objects.get(
                    id=employee_registration_form.cleaned_data['employee_type'])
                g.user_set.add(user)
                user.save()
                nts_list = NTS.objects.all()
                employee = Employee.objects.get(id=user.id)
                for nts in nts_list:
                    if employee_secret_key == nts.secret_key:
                        employee.id_nts = nts
                if employee.id_nts is None:
                    return render(request, 'employees/registration_decline_message.html')
                return render(request, 'employees/register_message.html', {'form': employee_registration_form})
            else:
                return render_form()
        else:
            return render_form()
    return HttpResponseRedirect('/')


def employee_logout(request):
    logout(request)
    return HttpResponseRedirect('/employees/login')



def _logout(request):
    logout(request)
    return HttpResponseRedirect('/login')
