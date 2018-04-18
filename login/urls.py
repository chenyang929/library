from django.urls import path, re_path
from . import views

app_name = 'login'
urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
]
