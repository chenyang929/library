from django.urls import path, re_path
from . import views

app_name = 'backend'
urlpatterns = [
    path('history', views.backend_history, name='backend_history'),
    path('storage', views.backend_storage, name='backend_storage'),
    path('user', views.backend_user, name='backend_user'),
    path('buy', views.backend_buy, name='backend_buy'),
    re_path(r'^$', views.index, name='index'),
]
