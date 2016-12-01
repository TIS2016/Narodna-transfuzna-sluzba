from django.conf.urls import url
from . import views

app_name = 'isnts'

handler404 = views.auth.error404


urlpatterns = [
    url(r'^donors/validate/(?P<donor_id>[0-9]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.auth.donor_activate),
    url(r'^donors/(?P<donor_id>[0-9]+)/$', views.donor.detailview),
    url(r'^donors/(?P<donor_id>[0-9]+)/questionnaire/(?P<questionnaire_id>[0-9]+)/$', views.donor.quastionnaire),
    url(r'^donors/(?P<donor_id>[0-9]+)/blood_extraction/(?P<blood_extraction_id>[0-9]+)/$', views.donor.blood_extraction),
    url(r'^donors/information/$', views.donor.information),
    url(r'^donors/$', views.donor.listview),
    url(r'^blood_extraction/(?P<blood_extraction_id>[0-9]+)/$', views.blood_extraction.detailview),
    url(r'^blood_extraction/$', views.blood_extraction.listview),
    url(r'^login/$', views.auth.donor_login),
    url(r'^logout/$', views.auth.donor_logout),
    url(r'^register/$', views.auth.donor_register),
    url(r'^pass_change/$', views.auth.donor_pass_change),
    url(r'^nopermission/$', views.auth.permission_denied),
    url(r'^$', views.donor.home)
]
