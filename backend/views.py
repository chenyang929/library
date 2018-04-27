from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from storage.models import Storage
from history.models import History
from django.http.response import HttpResponse


@login_required(login_url='login:login')
def index(request):
    history_lst = History.objects.filter(status__in=[1, 4])
    storage_lst = Storage.objects.filter(remain__gt=0)
    user_lst = User.objects.filter(is_staff=0)
    context = {"history_lst": history_lst, "storage_lst": storage_lst, "user_lst": user_lst}
    return render(request, "backend.html", context)


def backend_storage(request):
    storage_lst = Storage.objects.all()
    context = {"storage_lst": storage_lst}
    return render(request, 'backend_storage.html', context)


def backend_user(request):
    user_lst = User.objects.filter(is_staff=0).order_by('-id')
    context = {"user_lst": user_lst}
    return render(request, 'backend_user.html', context)


def backend_buy(request):
    return render(request, 'backend_buy.html')



