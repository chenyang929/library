import re
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .func import user_add
from .serializers import UserSerializers
from django.shortcuts import render
from history.models import History


def user_add_api(request):
    lst = list(user_add())
    for item in lst:
        email = item[0]
        username = item[1]
        User.objects.create_user(username=email, password=email, first_name=username, email=email).save()
    return HttpResponse("导入成功!")


def user_center(request):
    user_id = request.user.id
    history_lst = History.objects.filter(user=request.user, status=5)
    context = {"user_id": user_id, "user": request.user.first_name, "history_lst": history_lst}
    return render(request, 'user.html', context)


@api_view(['GET', 'POST'])
def user_list(request):
    if not request.user.is_superuser:
        return Response({"info": "权限禁止"}, status=403)
    if request.method == 'GET':
        user_lst = User.objects.filter(is_staff=0)
        count = user_lst.count()
        per_page_num = 20  # 每页显示15个
        page = 1
        page_str = re.findall(r'page=(\d+)', request.META.get('QUERY_STRING'))
        if page_str:
            page = int(page_str[0])
        mp = get_start_end(page, per_page_num, count)
        start = mp['start']
        end = mp['end']
        previous_page = mp['previous_page']
        next_page = mp['next_page']
        storage_per = user_lst[start:end]
        serializer = UserSerializers(storage_per, many=True)
        mp = {"counts": count, "results": serializer.data, "next_page": next_page, "previous_page": previous_page}
        return Response(mp)

    elif request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('name')
        if User.objects.filter(username=email):
            return Response({"info": "用户已存在"})
        if all([email, username]):
            User.objects.create_user(username=email, password=email, first_name=username, email=email).save()
            return Response({"info": "创建用户成功"}, status=201)
        return Response({"info": "用户信息缺失"}, status=501)


@api_view(['GET', 'POST'])   # POST DELETE 稍后
def user_detail(request, pk):
    if not request.user.is_authenticated:
        return Response({"info": "权限禁止"}, status=403)
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"info": "用户不存在"})
    if request.method == 'GET':
        serializers = UserSerializers(user)
        return Response(serializers.data)
    elif request.method == 'POST':   # 修改密码
        if request.user.is_superuser:
            user_name = request.POST.get('user_name')
            first_name = request.POST.get('first_name')
            pw = request.POST.get('pw')
            if all([user_name, first_name]):
                new_user = User.objects.filter(username=user_name)
                if new_user and int(new_user[0].id) != int(pk):
                    return Response({"info": "用户信息重复"})
                user.username = user_name
                user.first_name = first_name
                user.email = user_name
                if pw:
                    user.set_password(user_name)   # 重置密码
                user.save()
                return Response({"info": "用户信息修改成功"})
            else:
                return Response({"info": "用户信息不完整"})
        else:
            pw = request.POST.get('pw')
            if pw:
                user.set_password(pw)
                user.save()
                return Response({"info": "修改密码成功"})
            else:
                return Response({"info": "信息不完整"})


def get_start_end(page, per_page_num, count):
    if count < per_page_num:  # 总数目比每页显示数目还小
        start = 0
        end = count
        previous_page = next_page = None
    else:
        page = int(page)
        total_page = int(count / per_page_num)
        if int(count % per_page_num) != 0:
            total_page += 1
        previous_page = page - 1
        next_page = page + 1
        if page <= 1:
            page = 1
            previous_page = None
        if page >= total_page:
            page = total_page
            next_page = None
        start = (page - 1) * per_page_num
        end = page * per_page_num
    return {"start": start, "end": end, "previous_page": previous_page, "next_page": next_page}








