from django.conf.urls import url
from . import views

app_name = 'isnts'

handler404 = 'nts.views.my_custom_page_not_found_view'


urlpatterns = [
    url(r'^donors/(?P<donor_id>[0-9]+)/$', views.donor_detail),
    url(r'^donors/$', views.donor_listview),
    url(r'^blood_extraction/(?P<blood_extraction_id>[0-9]+)/$', views.blood_extraction_detailview),
    url(r'^blood_extraction/$', views.blood_extraction_listview),
    url(r'^login/$', views.donor_login),
    url(r'^logout/$', views.donor_logout),
    url(r'^register/$', views.donor_register),
    url(r'^pass_change/$', views.donor_pass_change),
    url(r'^donors/information/$', views.donor_information),
<<<<<<< HEAD
    url(r'^employees/(?P<employee_id>[0-9]+)/$', views.employee_detail),
    url(r'^employees/$', views.employee_listview),
    url(r'^employees/login/$', views.employee_login),
    url(r'^employees/register/$', views.employee_register),
    url(r'^employees/interface/$', views.employee_interface),
    url(r'^employees/logout/$', views.employee_logout),
=======
    url(r'^nopermission/$', views.permission_denied),
>>>>>>> master
    url(r'^$', views.home)
]
