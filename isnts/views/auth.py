from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.shortcuts import render
from django import forms, http
from isnts.models import *
from isnts.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.views import password_reset, password_reset_confirm
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
                user.is_active = False
                g = Group.objects.get(name='Donor')
                g.user_set.add(user)
                user.save()

                token = default_token_generator.make_token(user)
                context = Context({
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'donor_id': user.id,
                    'token': token
                })
                subject = 'Verification'

                text_content = get_template('emails/verification.txt').render(context)
                html_content = get_template('emails/verification.html').render(context)

                message = EmailMultiAlternatives(subject, text_content,'isntsdebug@gmail.com', [user.email])
                message.attach_alternative(html_content, "text/html")

                try:
                    message.send()
                except:
                    return HttpResponseRedirect("/verification_error")
                return render(request, 'donors/register.html', {'form': form})
            else:
                return render_form()
        else:
            return render_form()
    return HttpResponseRedirect('/donors/information/')


def donor_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')


def donor_activate(request, donor_id, token):
    if donor_id is not None and token is not None:
        try:
            user_model = get_user_model()
            user = user_model.objects.get(pk=donor_id)
            if default_token_generator.check_token(user, token) and (not user.is_active):
                user.is_active = True
                user.save()
                return HttpResponseRedirect("/success")
        except:
            pass
    return HttpResponseRedirect("/verification_error")

# Views below is defined for Donors and Employees

def password_change(request):
    form = PassChange()
    return render(request, 'donors/pass_change.html', {'form': form})


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
