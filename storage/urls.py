from django.urls import re_path
from . import views

app_name = 'storage'
urlpatterns = [
    re_path(r'^$', views.storage_list, name='storage_list'),
    re_path(r'(?P<pk>[0-9]+)$', views.storage_detail, name='storage_detail'),
    #re_path(r'(?P<pk>[0-9]+)/$', views.storage_detail, name='storage_detail'),
]
