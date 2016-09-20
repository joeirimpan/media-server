from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list/$', views.list, name='list')
     url(r'startserver',views.start_server,name="start_server"), 
     url(r'^$', views.scan_list, name="scan_list"),
]
