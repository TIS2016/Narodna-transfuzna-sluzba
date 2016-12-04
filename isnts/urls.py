from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


app_name = 'isnts'

handler404 = views.auth.error404


urlpatterns = [
    url(r'^donors/validate/(?P<donor_id>[0-9]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.auth.donor_activate),
    url(r'^donors/create_new/$', views.donor.create_new),
    url(r'^donors/(?P<donor_id>[0-9]+)/$', views.donor.detailview),
    url(r'^donors/(?P<donor_id>[0-9]+)/questionnaire/(?P<questionnaire_id>[0-9]+)/$', views.donor.quastionnaire),
    url(r'^donors/(?P<donor_id>[0-9]+)/blood_extraction/(?P<blood_extraction_id>[0-9]+)/$', views.donor.blood_extraction),
    url(r'^donors/information/$', views.donor.information),
    url(r'^donors/$', views.donor.listview),
    url(r'^blood_extraction/(?P<blood_extraction_id>[0-9]+)/$', views.blood_extraction.detailview),
    url(r'^blood_extraction/$', views.blood_extraction.listview),
    url(r'^login/$', views.auth.donor_login, name='login'),
    url(r'^logout/$', views.auth.donor_logout),
    url(r'^register/$', views.auth.donor_register),
    url(r'^password_change/$', views.auth.password_change, name="log"),
    url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.auth._password_reset_confirm),
    url(r'^password_reset/$', views.auth._password_reset),
    url(r'^password_reset_sent/$', views.auth.password_reset_sent),
    url(r'^nopermission/$', views.auth.permission_denied),
    url(r'^$', views.donor.home)
]
