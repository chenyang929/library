from django.urls import path, re_path
from . import views

app_name = 'storage'
urlpatterns = [
    path('user_add_api', views.user_add_api, name='user_add_api'),   # 添加用户
    path('center', views.user_center, name='user_center'),
    re_path(r'^$', views.index, name='index'),
]