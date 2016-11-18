from django.conf.urls import url
from . import views

app_name = 'isnts'

handler404 = 'nts.views.my_custom_page_not_found_view'


urlpatterns = [
    url(r'^donors/(?P<donor_id>[0-9]+)/$', views.donor_detail),
    url(r'^donors/$', views.donor_listview),
    url(r'^login/$', views.donor_login),
    url(r'^$', views.home)
]
