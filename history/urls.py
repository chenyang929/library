from django.urls import path, re_path
from . import views

app_name = 'history'
urlpatterns = [
    re_path(r'^$', views.history_list, name='history_list'),
    re_path(r'(?P<pk>[0-9]+)$', views.history_detail, name='history_detail'),
]
