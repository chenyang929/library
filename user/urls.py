from django.urls import path, re_path
from . import views

app_name = 'user'
urlpatterns = [
    path('user_add_api/', views.user_add_api, name='user_add_api'),
    path('center', views.user_center, name='user_center'),
    re_path('(?P<pk>[0-9]+)$', views.user_detail, name='user_detail'),
    path('', views.user_list, name='user_list'),
]
