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
        serializers = UserSerializers(user_lst, many=True)
        return Response(serializers.data)
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
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"info": "用户不存在"})
    if not request.user == user:
        return Response({"info": "权限禁止"}, status=403)
    if request.method == 'GET':
        serializers = UserSerializers(user)
        return Response(serializers.data)
    elif request.method == 'POST':   # 修改密码
        pw = request.POST.get('pw')
        if pw:
            user.set_password(pw)
            user.save()
            return Response({"info": "修改密码成功"})
        else:
            return Response({"info": "信息不完整"})












