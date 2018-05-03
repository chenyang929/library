from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from storage.models import Storage
from history.models import History


@login_required(login_url='login:login')
def index(request):
    history_lst = History.objects.filter(status__in=[1, 4])
    context = {"history_lst": history_lst, }
    return render(request, "backend.html", context)


def backend_history(request):
    storage_lst = Storage.objects.filter(remain__gt=0)
    user_lst = User.objects.filter(is_staff=0)
    history_lst = History.objects.all().order_by('-id')
    count = history_lst.count()
    total_page = int(count / 15)
    if int(count % 15) != 0:
        total_page += 1
    context = {"history_lst": history_lst, "total_page": total_page, "storage_lst": storage_lst, "user_lst": user_lst}
    if total_page > 1:
        context.update({"next_page": '/library/api/history?page=2'})
    return render(request, "backend_history.html", context)


def backend_storage(request):
    storage_lst = Storage.objects.all()
    count = storage_lst.count()
    total_page = int(count / 15)
    if int(count % 15) != 0:
        total_page += 1
    context = {"storage_lst": storage_lst[:15], "total_page": total_page, "next_page": '/library/api/storage?page=2'}
    return render(request, 'backend_storage.html', context)


def backend_user(request):
    user_lst = User.objects.filter(is_staff=0).order_by('-id')
    count = user_lst.count()
    total_page = int(count / 15)
    if int(count % 15) != 0:
        total_page += 1
    context = {"user_lst": user_lst[:15], "total_page": total_page, "next_page": '/library/api/user?page=2'}
    return render(request, 'backend_user.html', context)


def backend_buy(request):
    return render(request, 'backend_buy.html')



