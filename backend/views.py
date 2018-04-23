from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from storage.models import Storage
from history.models import History
from django.http.response import HttpResponse


@login_required(login_url='login:login')
def index(request):
    history_lst = History.objects.filter(status__in=[1, 4])
    context = {"history_lst": history_lst, "user": request.user.first_name}
    return render(request, "backend.html", context)


def storage_list(request):
    storage_lst = Storage.objects.all()
    for storage in storage_lst:
        history = History.objects.filter(book=storage).last()
        if history:
            user = history.user.first_name
            print(user)
    return HttpResponse('hello')

