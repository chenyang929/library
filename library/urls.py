"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from storage.views import index, backend

urlpatterns = [
    path('library/', index),
    path('library/backend/', backend),
    path('library/user/', include('user.urls')),
    path('library/login/', include('login.urls')),
    path('library/storage', include('storage.urls')),
    path('library/history/', include('history.urls')),
    path('admin/', admin.site.urls),
]
