from django.conf.urls import url
from . import views

app_name = 'isnts'

handler404 = views.auth.error404


urlpatterns = [
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
    url(r'^logout/$', views.auth.donor_logout),
    url(r'^register/$', views.auth.donor_register),
    url(r'^password_change/$', views.auth.donor_password_change),
    url(r'^nopermission/$', views.auth.permission_denied),
    url(r'^$', views.donor.home)
]
