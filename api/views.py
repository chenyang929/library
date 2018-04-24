import datetime
import re
from urllib import parse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, StorageSerializer, HistorySerializer
from storage.models import Storage
from history.models import History

"""
用户API
GET /user   获取全部用户信息   admin
POST email=email name=name /user   新建用户   admin
GET /user/1   获取单条用户信息   user admin
POST user_name=user_name first_name=first_name pw=pw /user/1   修改单条用户信息   user admin
"""


@api_view(['GET', 'POST'])
def user_list(request):
    if not request.user.is_superuser:
        return Response({"info": "权限禁止"}, status=403)
    if request.method == 'GET':
        search_str = re.findall(r'search=(.+)', request.META.get('QUERY_STRING'))
        if search_str:
            search_str = parse.unquote(search_str[0])
            user_lst = User.objects.filter(first_name__icontains=search_str)
        else:
            user_lst = User.objects.filter(is_staff=0)
        per_page_num = 15  # 每页显示15个
        page = 1
        page_str = re.findall(r'page=(\d+)', request.META.get('QUERY_STRING'))
        if page_str:
            page = int(page_str[0])
        mp = per_page(user_lst, per_page_num, page, UserSerializer)
        return Response(mp)

    elif request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('name')
        if User.objects.filter(username=email):
            return Response({"info": "用户已存在"})
        if all([email, username]):
            new_user = User.objects.create_user(username=email, password=email, first_name=username, email=email)
            serializers = UserSerializer(new_user)
            return Response({"info": "success", "results": [serializers.data]}, status=201)
        return Response({"info": "用户信息缺失"}, status=501)


@api_view(['GET', 'POST'])
def user_detail(request, pk):
    if not request.user.is_authenticated:
        return Response({"info": "权限禁止"}, status=403)
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"info": "用户不存在"})
    if request.method == 'GET':
        serializers = UserSerializer(user)
        return Response({"info": "success", "results": [serializers.data]})
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
                serializers = UserSerializer(user)
                return Response({"info": "success", "results": [serializers.data]}, status=201)
            else:
                return Response({"info": "用户信息不完整"}, status=501)
        else:
            pw = request.POST.get('pw')
            if pw:
                user.set_password(pw)
                user.save()
                serializers = UserSerializer(user)
                return Response({"info": "success", "results": [serializers.data]}, status=201)
            else:
                return Response({"info": "信息不完整"}, status=501)


"""
库存API
GET /storage   获取全部图书库存信息   user admin
POST book=book /storage   新书入库   admin
GET /storage/1   获取单条库存信息   user admin
POST /storage/1   修改单条库存信息   admin
"""


@api_view(['GET', 'POST'])
def storage_list(request):
    if not request.user.is_authenticated:
        return Response({"info": "权限禁止"}, status=403)
    if request.method == 'GET':   # 获取库存列表
        search_str = re.findall(r'search=(.+)', request.META.get('QUERY_STRING'))
        remain_str = re.findall(r'remain=(\d+)', request.META.get('QUERY_STRING'))
        if search_str:
            search_str = parse.unquote(search_str[0])
            storage_lst = Storage.objects.filter(book__icontains=search_str)
        elif remain_str and int(remain_str[0]) in (0, 1):
            storage_lst = Storage.objects.filter(remain=int(remain_str[0]))
        else:
            storage_lst = Storage.objects.all()
        per_page_num = 15  # 每页显示15个
        page = 1
        page_str = re.findall(r'page=(\d+)', request.META.get('QUERY_STRING'))
        if page_str:
            page = int(page_str[0])
        mp = per_page(storage_lst, per_page_num, page, StorageSerializer)
        return Response(mp)

    elif request.method == 'POST':   # 新书入库
        if not request.user.is_superuser:
            return Response({"info": "权限禁止"}, status=403)
        book = request.POST.get('book')
        inventory = request.POST.get('inventory')
        if book and inventory:
            if Storage.objects.filter(book=book):
                return Response({"info": "图书已存在"})
            new_storage = Storage.objects.create(book=book, inventory=inventory)
            serializers = StorageSerializer(new_storage)
            return Response({"info": "success", "results": [serializers.data]}, status=201)
        else:
            return Response({"info": "图书信息缺失"}, status=501)


@api_view(['GET', 'POST'])
def storage_detail(request, pk):
    if not request.user.is_authenticated:
        return Response({"info": "权限禁止"}, status=403)
    try:
        storage = Storage.objects.get(pk=pk)
    except Storage.DoesNotExist:
        return Response({"info": "图书不存在"})
    if request.method == 'GET':   # 获取图书详情
        serializers = StorageSerializer(storage)
        return Response({"info": "success", "results": [serializers.data]})
    elif request.method == 'POST':   # 修改图书信息
        if not request.user.is_superuser:
            return Response({"info": "权限禁止"}, status=403)
        book = request.POST.get('book')
        inventory = request.POST.get('inventory')
        remain = request.POST.get('remain')
        if all([book, inventory, remain]):
            new_storage = Storage.objects.filter(book=book)
            if new_storage and int(new_storage[0].id) != int(pk):
                return Response({"info": "图书已存在"})
            storage.book = book
            storage.inventory = inventory
            storage.remain = remain
            storage.save()
            serializers = StorageSerializer(storage)
            return Response({"info": "success", "results": [serializers.data]}, status=201)
        else:
            return Response({"info": "图书信息缺失"}, status=501)
    elif request.method == 'DELETE':
        storage = Storage.objects.get(pk=pk)
        storage.is_delete = 1
        storage.save()
        return Response({"info": "删除成功"},)


"""
借阅记录API
GET /history   获取借阅记录   user admin
POST /history   新增借阅记录   user admin
GET /history/1   获取单条借阅记录   user admin
POST msg=msg delay=delay /history/1   修改单条借阅记录   user admin
"""


@api_view(['GET', 'POST'])
def history_list(request):
    if not request.user.is_authenticated:
        return Response({"info": "权限禁止"}, status=403)
    if request.method == 'GET':
        if request.user.is_superuser:
            history_lst = History.objects.all()
        else:
            history_lst = History.objects.filter(user=request.user)
        per_page_num = 15  # 每页显示15个
        page = 1
        page_str = re.findall(r'page=(\d+)', request.META.get('QUERY_STRING'))
        if page_str:
            page = int(page_str[0])
        mp = per_page(history_lst, per_page_num, page, HistorySerializer)
        return Response(mp)
    elif request.method == 'POST':
        storage_id = request.POST.get('storage_id')
        try:
            storage = Storage.objects.get(pk=storage_id)
        except Storage.DoesNotExist:
            return Response({"info": "图书不存在"})
        my_history_list = History.objects.filter(user=request.user, status__in=[1, 2, 3, 4])
        if len(my_history_list) >= 2:
            return Response({"info": "当前已借阅两本图书!"})
        remain = storage.remain
        if remain > 0:
            storage.remain = remain - 1
            storage.save()
            new_history = History.objects.create(book=storage, user=request.user)
            serializers = HistorySerializer(new_history)
            return Response({"info": "success", "results": [serializers.data]}, status=201)
        else:
            return Response({"info": "ops!手慢了"})


@api_view(['GET', 'POST'])
def history_detail(request, pk):
    if not request.user.is_authenticated:
        return Response({"info": "权限禁止"}, status=403)
    try:
        history = History.objects.get(pk=pk)
    except History.DoesNotExist:
        return Response({"info": "记录不存在"})
    if request.method == 'POST':
        status_old = history.status
        if request.user.is_superuser:
            if status_old in (1, 4):
                msg = request.POST.get("msg")
                if msg and msg == 'yes':
                    history.status += 1
                    if status_old == 4:   # 还书后把库存加1
                        history.back_date = datetime.date.today()
                        storage = Storage.objects.get(pk=history.book_id)
                        storage.remain += 1
                        storage.save()
                elif msg and msg == 'no':
                    history.status -= 1
                    if status_old == 1:   # 借阅不同意后把库存加1
                        storage = Storage.objects.get(pk=history.book_id)
                        storage.remain += 1
                        storage.save()
        elif history.user == request.user:
                delay = request.POST.get('delay')
                if delay and status_old == 2:
                    history_delay = history.delay
                    history.delay = int(history_delay) ^ 1
                elif status_old == 2:
                    history.status = 4
        history.save()
        serializers = HistorySerializer(history)
        return Response({"info": "success", "results": [serializers.data]}, status=201)
    elif request.method == 'GET':
        serializers = HistorySerializer(history)
        return Response({"info": "success", "results": [serializers.data]})


def per_page(lst, per_page_num, page, serializer):
    count = lst.count()
    mp = get_start_end(page, per_page_num, count)
    start = mp['start']
    end = mp['end']
    previous_page = mp['previous_page']
    next_page = mp['next_page']
    lst_per = lst[start:end]
    my_serializer = serializer(lst_per, many=True)
    mp = {"info": "success", "counts": count, "results": my_serializer.data, "next_page": next_page,
          "previous_page": previous_page}
    return mp


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

