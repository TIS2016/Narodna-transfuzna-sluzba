from django.conf.urls import url
from . import views

app_name = 'isnts'

handler404 = 'nts.views.my_custom_page_not_found_view'


urlpatterns = [
    url(r'^donors/(?P<donor_id>[0-9]+)/$', views.donor_detail),
    url(r'^donors/(?P<donor_id>[0-9]+)/(?P<questionnaire_id>[0-9]+)/$', views.donor_quastionnare),
    url(r'^donors/$', views.donor_listview),
    url(r'^blood_extraction/(?P<blood_extraction_id>[0-9]+)/$', views.blood_extraction_detailview),
    url(r'^blood_extraction/$', views.blood_extraction_listview),
    url(r'^login/$', views.donor_login),
    url(r'^logout/$', views.donor_logout),
    url(r'^donors/information/$', views.donor_information),
    url(r'^$', views.home)
]
