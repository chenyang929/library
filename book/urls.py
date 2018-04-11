from django.urls import path, re_path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.index),
    re_path('api/book/page=(?P<page>[0-9]+)/$', views.book_list_api),
    re_path(r'api/book/status=(?P<status>[0-9]+)/page=(?P<page>[0-9]+)/$', views.book_list_filter_api),
    re_path(r'api/book/(?P<pk>[0-9]+)/$', views.book_detail_api),
    re_path(r'api/back/(?P<pk>[0-9]+)/$', views.book_back),
    path('api/history/', views.history_list_api),
    re_path(r'api/history/(?P<pk>[0-9]+)/$', views.history_detail_api),
    re_path('api/manage/check/(?P<pk>[0-9]+)/$', views.check),
    path('api/manage/add/', views.book_add),
]
