from django.urls import path, re_path
from . import views

app_name = 'api'
urlpatterns = [
    re_path('user/(?P<pk>[0-9]+)$', views.user_detail, name='user_detail'),
    re_path('user', views.user_list, name='user_list'),
    re_path(r'storage/(?P<pk>[0-9]+)$', views.storage_detail, name='storage_detail'),
    re_path(r'storage', views.storage_list, name='storage_list'),
    re_path(r'history/(?P<pk>[0-9]+)$', views.history_detail, name='history_detail'),
    re_path(r'history', views.history_list, name='history_list'),
]
