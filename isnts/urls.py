from django.conf.urls import url
from . import views

app_name = 'isnts'

urlpatterns = [
    url(r'^donors_detail/$', views.donor_detail, name='donors_detail'),
    url(r'^donors/$', views.donor_listview, name='donors'),
    url(r'^$', views.home, name='home')
]
