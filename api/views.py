import datetime
import re
from urllib import parse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, StorageSerializer, HistorySerializer
from storage.models import Storage
from history.models import History

PER = 15   # 分页显示每页数量

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
        query_str, page, per = get_new_query(request.META.get('QUERY_STRING'))
        search_str = re.findall(r'name=(.+)&?', query_str)
        if search_str:
            search_str = parse.unquote(search_str[0].split('&')[0])
            user_lst = User.objects.filter(first_name__icontains=search_str)
        else:
            user_lst = User.objects.filter(is_staff=0)
        mp = get_format_results(query_str, page, per, user_lst, UserSerializer, request.META.get('PATH_INFO'))
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
                    return Response({"info": "用户已存在"})
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
        query_str, page, per = get_new_query(request.META.get('QUERY_STRING'))
        search_str = re.findall(r'book=(.+)&?', query_str)
        remain_str = re.findall(r'remain=(\d+)', query_str)
        if search_str:
            search_str = parse.unquote(search_str[0].split('&')[0])
            storage_lst = Storage.objects.filter(book__icontains=search_str)
        elif remain_str and int(remain_str[0]) in (0, 1):
            storage_lst = Storage.objects.filter(remain=int(remain_str[0]))
        else:
            storage_lst = Storage.objects.all()
        mp = get_format_results(query_str, page, per, storage_lst, StorageSerializer, request.META.get('PATH_INFO'))
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
        query_str, page, per = get_new_query(request.META.get('QUERY_STRING'))
        if request.user.is_superuser:
            user_str = re.findall(r'user=(.+)&?', query_str)
            book_str = re.findall(r'book=(.+)&?', query_str)
            print(book_str)
            if user_str:
                user_str = parse.unquote(user_str[0].split('&')[0])
                history_lst = History.objects.filter(user__first_name=user_str)
            elif book_str:
                book_str = parse.unquote(book_str[0].split('&')[0])
                history_lst = History.objects.filter(book__book=book_str)
            else:
                history_lst = History.objects.all()
        else:
            history_lst = History.objects.filter(user=request.user)
        mp = get_format_results(query_str, page, per, history_lst, HistorySerializer, request.META.get('PATH_INFO'))
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
                delay = request.POST.get('delay')   # 续借
                if delay and status_old == 2:
                    history_delay = history.delay
                    history.delay = int(history_delay) ^ 1
                elif status_old in [2, 3]:
                    history.status = 4
        history.save()
        serializers = HistorySerializer(history)
        return Response({"info": "success", "results": [serializers.data]}, status=201)
    elif request.method == 'GET':
        serializers = HistorySerializer(history)
        return Response({"info": "success", "results": [serializers.data]})


def get_new_query(query_str):
    if query_str and ('page' not in query_str):
        query_str += '&page=1'
    elif not query_str:
        query_str = 'page=1'
    print(query_str)
    page = int(re.findall(r'page=(\d+)', query_str)[0])
    per_str = re.findall(r'per=(\d+)', query_str)
    per = int(per_str[0]) if per_str else PER
    return query_str, page, per


def get_start_end(page, per, count):
    if count < per:  # 总数目比每页显示数目还小
        total_page = 1 if count > 0 else 0
        start = 0
        end = count
        previous_page = next_page = None
    else:
        total_page = int(count / per)
        if int(count % per) != 0:
            total_page += 1
        previous_page = page - 1
        next_page = page + 1
        if page <= 1:
            page = 1
            previous_page = None
        if page >= total_page:
            page = total_page
            next_page = None
        start = (page - 1) * per
        end = page * per
    return {"start": start, "end": end, "count": count, "total_page": total_page, "per": per,
            "previous_page": previous_page, "next_page": next_page, "page": page}


def get_format_results(query_str, page, per, lst, serializer, path):
    count = lst.count()
    mp = get_start_end(page, per, count)
    next_page = mp['next_page']
    previous_page = mp['previous_page']
    if next_page:
        mp['next_page'] = get_next_previous_page_link(next_page, query_str, path)
    if previous_page:
        mp['previous_page'] = get_next_previous_page_link(previous_page, query_str, path)
    lst_per = lst[mp['start']:mp['end']]
    my_serializer = serializer(lst_per, many=True)
    mp.pop('start')
    mp.pop('end')
    mp.update({"info": "success", "results": my_serializer.data})
    return mp


def get_next_previous_page_link(page, query_str, path):
    page_str = 'page={}'.format(page)
    link = '{}?{}'.format(path, re.sub(r'page=(\d+)', page_str, query_str))
    return link

