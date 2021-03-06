import random
from .models import Storage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from .func import user_add
from django.shortcuts import render
from history.models import History
from .proverb import words


@login_required(login_url='login:login')
def index(request):
    print(request)
    print('-'*20)
    ss = request.session
    print(dict(ss))
    storage_lst = Storage.objects.all()
    count = storage_lst.count()
    total_page = int(count / 15)
    if int(count % 15) != 0:
        total_page += 1
    history_lst = History.objects.filter(user_id=request.user.pk, status__in=[1, 2, 3, 4])
    word = random.choice(words)
    context = {"storage_lst": storage_lst[:15], "count": storage_lst.count(), "history_lst": history_lst,
               "user": request.user.first_name, "total_page": total_page, "next_page": '/library/api/storage?page=2',
               'word': word}
    return render(request, "index.html", context)


def user_add_api(request):
    if request.user.is_superuser:
        lst = list(user_add())
        for item in lst:
            email = item[0]
            username = item[1]
            User.objects.create_user(username=email, password=email, first_name=username, email=email).save()
        msg = '用户导入成功'
    else:
        msg = '权限禁止'
    return HttpResponse(msg)


@login_required(login_url='login:login')
def user_center(request):
    user_id = request.user.id
    history_lst = History.objects.filter(user_id=request.user.pk, status=5)
    word = random.choice(words)
    context = {"user_id": user_id, "user": request.user.first_name, "history_lst": history_lst, "word": word}
    return render(request, 'user.html', context)
