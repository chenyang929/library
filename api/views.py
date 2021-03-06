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
GET /user/1   获取某条用户信息   user admin
POST user_name=user_name first_name=first_name pw=pw /user/1   修改某条用户信息   user admin
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
        email = request.POST.get('email').strip()
        username = request.POST.get('name').strip()
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
    elif request.method == 'POST':
        if request.user.is_superuser:
            user_name = request.POST.get('user_name')
            first_name = request.POST.get('first_name')
            pw = request.POST.get('pw')
            if pw and int(pw) == 1:
                user.set_password(user_name)  # 重置密码
                user.save()
                serializers = UserSerializer(user)
                return Response({"info": "success", "results": [serializers.data]}, status=201)
            elif all([user_name, first_name]):
                new_user = User.objects.filter(username=user_name)
                if new_user and int(new_user[0].id) != int(pk):
                    return Response({"info": "用户已存在"})
                user.username = user_name
                user.first_name = first_name
                user.email = user_name
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
GET /storage/1   获取某条库存信息   user admin
POST book=book inventory=inventory remain=remain /storage/1   修改某条库存信息   admin
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
        book = request.POST.get('book').strip()
        inventory = request.POST.get('inventory').strip()
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
GET /history/1   获取某条借阅记录   user admin
POST status=status delay=delay /history/1   修改某条借阅记录   user admin
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
            status_str = re.findall(r'status=(\d+)', query_str)
            if user_str:
                user_str = parse.unquote(user_str[0].split('&')[0])
                history_lst = History.objects.filter(user__icontains=user_str)
            elif book_str:
                book_str = parse.unquote(book_str[0].split('&')[0])
                history_lst = History.objects.filter(book__icontains=book_str)
            elif status_str and int(status_str[0]) in list(range(6)):
                history_lst = History.objects.filter(status=int(status_str[0]))
            else:
                history_lst = History.objects.all()
        else:
            history_lst = History.objects.filter(user_id=request.user.id)
        mp = get_format_results(query_str, page, per, history_lst, HistorySerializer, request.META.get('PATH_INFO'))
        return Response(mp)
    elif request.method == 'POST':
        storage_id = request.POST.get('storage_id')
        try:
            storage = Storage.objects.get(pk=storage_id)
        except Storage.DoesNotExist:
            return Response({"info": "图书不存在"})
        remain = storage.remain
        if remain == 0:
            return Response({"info": "图书库存不足，无法借阅"})
        if request.user.is_superuser:
            user_id = request.POST.get('user_id')
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return Response({"info": "用户不存在"})
            borrow_date = request.POST.get('borrow_date')
            storage.remain = remain - 1
            storage.save()
            back_date = datetime.datetime.strptime(borrow_date, '%Y-%m-%d') + datetime.timedelta(days=30)
            back_date = back_date.strftime('%Y-%m-%d').split(' ')[0]
            new_history = History.objects.create(book=storage.book, book_id=storage.id,
                                                 user=user.first_name, user_id=user.id,
                                                 borrow_date=borrow_date, back_date=back_date, status=2)
            serializers = HistorySerializer(new_history)
            return Response({"info": "success", "results": [serializers.data]}, status=201)
        else:
            my_history_list = History.objects.filter(user_id=request.user.id,
                                                     status__in=[1, 2, 3, 4])
            if len(my_history_list) >= 2:
                return Response({"info": "当前已借阅两本图书!"})
            storage.remain = remain - 1
            storage.save()
            borrow_date = datetime.date.today()
            new_history = History.objects.create(book=storage.book, book_id=storage.id, borrow_date=borrow_date,
                                                 user=request.user.first_name, user_id=request.user.id)
            serializers = HistorySerializer(new_history)
            return Response({"info": "success", "results": [serializers.data]}, status=201)


@api_view(['GET', 'POST'])
def history_detail(request, pk):
    try:
        history = History.objects.get(pk=pk)
    except History.DoesNotExist:
        return Response({"info": "记录不存在"})
    status_old = history.status
    if request.user.is_superuser or all([request.user.is_authenticated, request.user.pk == history.user_id]):
        if request.method == 'GET':
            serializers = HistorySerializer(history)
            return Response({"info": "success", "results": [serializers.data]})
        elif request.method == 'POST':
            if not request.user.is_superuser and status_old not in [2, 3]:
                return Response({"info": "权限禁止"}, status=403)
            status_new = request.POST.get('status')
            delay = request.POST.get('delay')
            if status_old in [0, 5]:
                pass
            elif status_new and int(status_new) in list(range(6)):
                history.status = int(status_new)
                if not history.back_date:
                    history.back_date = history.borrow_date + datetime.timedelta(days=30)
                if int(status_new) in [0, 5]:   # 借阅不通过或是还书
                    storage = Storage.objects.get(pk=history.book_id)
                    storage.remain += 1
                    storage.save()
                    if int(status_new) == 5:
                        history.back_date = datetime.date.today()
            if int(status_old) == 2 and delay and int(delay) in [0, 1]:
                history.delay = delay
                borrow_date = history.borrow_date
                if int(delay) == 0:
                    history.back_date = borrow_date + datetime.timedelta(days=30)
                else:
                    history.back_date = borrow_date + datetime.timedelta(days=60)
            history.save()
            serializers = HistorySerializer(history)
            return Response({"info": "success", "results": [serializers.data]}, status=201)
    else:
        return Response({"info": "权限禁止"}, status=403)


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

