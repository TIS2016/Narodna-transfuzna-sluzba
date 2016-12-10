from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


app_name = 'isnts'

handler404 = views.auth.error404


urlpatterns = [
    url(r'^donors/terms/(?P<nts_id>[0-9]+)/$', views.donor.terms_choose_day),
    url(r'^donors/terms/$', views.donor.terms_choose_nts),
    url(r'^donors/terms/list/$', views.donor.terms_listview),
    url(r'^donors/create_new/$', views.donor.create_new),
    url(r'^donors/(?P<donor_id>[0-9]+)/$', views.donor.detailview),
    url(r'^donors/(?P<donor_id>[0-9]+)/questionnaire/(?P<questionnaire_id>[0-9]+)/$', views.donor.quastionnaire),
    url(r'^donors/(?P<donor_id>[0-9]+)/blood_extraction/(?P<blood_extraction_id>[0-9]+)/$', views.donor.blood_extraction),
    url(r'^donors/information/$', views.donor.information),
    url(r'^donors/$', views.donor.listview),
    url(r'^employees/(?P<employee_id>[0-9]+)/$', views.employee.detailview),
    url(r'^employees/$', views.employee.listview),
    url(r'^employees/login/$', views.auth.employee_login),
    url(r'^employees/register/$', views.auth.employee_register),
    url(r'^employees/interface/$', views.employee.interface),
    url(r'^employees/logout/$', views.auth.employee_logout),
    url(r'^blood_extraction/(?P<blood_extraction_id>[0-9]+)/$', views.blood_extraction.detailview),
    url(r'^blood_extraction/$', views.blood_extraction.listview),
    url(r'^login/$', views.auth.donor_login),
    url(r'^logout/$', views.auth._logout),
    url(r'^registration/confirm/(?P<donor_id>[0-9]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.auth.donor_registration_confirm),
    url(r'^registration/$', views.auth.donor_registration),
    url(r'^registration/success/$', views.auth.donor_registration_success),
    url(r'^password_change/$', views.auth.password_change),
    url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.auth._password_reset_confirm),
    url(r'^password_reset/$', views.auth._password_reset),
    url(r'^password_reset_sent/$', views.auth.password_reset_sent),
    url(r'^nopermission/$', views.auth.permission_denied),
    url(r'^$', views.donor.home)
]
