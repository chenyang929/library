from urllib import parse
from django.shortcuts import render
from .models import Storage
from .serializers import StorageSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
import re
from django.contrib.auth.decorators import login_required
from history.models import History


@login_required(login_url='login:login')
def index(request):
    storage_lst = Storage.objects.all()
    history_lst = History.objects.filter(user=request.user, status__in=[1, 2, 4])
    context = {"storage_lst": storage_lst[:15], "count": storage_lst.count(), "history_lst": history_lst,
               "user": request.user.first_name}
    return render(request, "index.html", context)


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
        count = storage_lst.count()
        per_page_num = 15   # 每页显示15个
        page = 1
        page_str = re.findall(r'page=(\d+)', request.META.get('QUERY_STRING'))
        if page_str:
            page = int(page_str[0])
        mp = get_start_end(page, per_page_num, count)
        start = mp['start']
        end = mp['end']
        previous_page = mp['previous_page']
        next_page = mp['next_page']
        storage_per = storage_lst[start:end]
        serializer = StorageSerializer(storage_per, many=True)
        mp = {"counts": count, "results": serializer.data, "next_page": next_page, "previous_page": previous_page}
        return Response(mp)

    elif request.method == 'POST':   # 新书入库
        if not request.user.is_superuser:
            return Response({"info": "权限禁止"}, status=403)
        book = request.POST.get('book')
        if book:
            if Storage.objects.filter(book=book):
                return Response({"info": "图书已存在"})
            Storage.objects.create(book=book).save()
            return Response({"info": "入库成功"}, status=201)
        else:
            return Response({"info": "图书信息缺失"})


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
        return Response(serializers.data)
    elif request.method == 'POST':   # 修改图书信息
        if not request.user.is_superuser:
            return Response({"info": "权限禁止"}, status=403)
        book = request.POST.get('book')
        inventory = request.POST.get('inventory')
        remain = request.POST.get('remain')
        if all([book, inventory, remain]):
            if Storage.objects.filter(book=book):
                return Response({"info": "图书已存在"})
            storage.book = book
            storage.inventory = inventory
            storage.remain = remain
            storage.save()
            return Response({"info": "图书信息修改成功"})
        else:
            return Response({"info": "图书信息缺失"})
    elif request.method == 'DELETE':
        storage = Storage.objects.get(pk=pk)
        storage.is_delete = 1
        storage.save()
        return Response({"info": "删除成功"},)



