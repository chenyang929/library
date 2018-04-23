from django.urls import path, re_path
from . import views

app_name = 'backend'
urlpatterns = [
    path('storage', views.storage_list, name='storage_list'),
    re_path(r'^$', views.index, name='index'),
]
