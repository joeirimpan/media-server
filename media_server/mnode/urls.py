from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.scan_list, name='scan_list'),
    url(r'^list/$', views.list, name='list')
]
