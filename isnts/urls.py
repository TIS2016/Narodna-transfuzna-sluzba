from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


app_name = 'isnts'

handler404 = views.auth.error404


urlpatterns = [
    url(r'^donors/create_new/$', views.donor.create_new, name="donors"),
    url(r'^donors/(?P<donor_id>[0-9]+)/$', views.donor.detailview, name="donors"),
    url(r'^donors/(?P<donor_id>[0-9]+)/questionnaire/(?P<questionnaire_id>[0-9]+)/$', views.donor.quastionnaire, name="donors"),
    url(r'^donors/(?P<donor_id>[0-9]+)/blood_extraction/(?P<blood_extraction_id>[0-9]+)/$', views.donor.blood_extraction, name="donors"),
    url(r'^donors/information/$', views.donor.information, name="information"),
    url(r'^donors/terms/(?P<nts_id>[0-9]+)/$', views.donor.terms_choose_day, name="terms"),
    url(r'^donors/terms/$', views.donor.terms_choose_nts, name="terms"),
    url(r'^donors/terms/list/$', views.donor.terms_listview, name="my_terms"),
    url(r'^donors/terms/remove/(?P<booking_id>[0-9]+)/$', views.donor.terms_remove),
    url(r'^donors/my_profile/', views.donor.my_profile),
    url(r'^donors/$', views.donor.listview, name="donors"),
    url(r'^employees/(?P<employee_id>[0-9]+)/$', views.employee.detailview, name="employees"),
    url(r'^employees/$', views.employee.listview, name="employees"),
    url(r'^employees/login/$', views.auth.employee_login, name="employees"),
    url(r'^employees/officehours/$', views.employee.office_hours, name="office_hours"),
    url(r'^employees/register/$', views.auth.employee_register, name="employees"),
    url(r'^employees/interface/$', views.employee.interface, name="employees"),
    url(r'^employees/terms', views.employee.terms_list, name="terms"),
    url(r'^logout/$', views.auth._logout, name="employees"),
    url(r'^superuser/secret_key_change/$', views.superuser.secret_key_change, name="superuser_keychange"),
    url(r'^superuser/employee_administration/$', views.superuser.employee_administration, name="superuser_administration"),
    url(r'^superuser/employee_administration/(?P<employee_id>[0-9]+)/$', views.superuser.employee_activation, name="superuser_administration"),
    url(r'^blood_extraction/(?P<blood_extraction_id>[0-9]+)/$', views.blood_extraction.detailview, name="blood_extraction"),
    url(r'^blood_extraction/$', views.blood_extraction.listview, name="blood_extraction"),
    url(r'^login/$', views.auth.donor_login),
    url(r'^registration/confirm/(?P<donor_id>[0-9]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.auth.donor_registration_confirm),
    url(r'^registration/$', views.auth.donor_registration),
    url(r'^password_change/$', views.auth.password_change),
    url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.auth._password_reset_confirm),
    url(r'^password_reset/$', views.auth._password_reset),
    url(r'^password_reset_sent/$', views.auth.password_reset_sent),
    url(r'^nopermission/$', views.auth.permission_denied),
    url(r'^$', views.donor.home)
]
