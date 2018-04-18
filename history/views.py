from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import History
from .serializers import HistorySerializer
from django.shortcuts import render
from django.contrib.auth.models import User
import datetime
from storage.models import Storage


@api_view(['GET', 'POST'])
def history_list(request):
    if not request.user.is_authenticated:
        return Response({"info": "权限禁止"}, status=403)
    if request.method == 'GET':
        if request.user.is_superuser:
            histories = History.objects.all()
        else:
            histories = History.objects.filter(user=request.user, status__in=[1, 2, 4])
        if histories:
            serializer = HistorySerializer(histories, many=True)
            histories = serializer.data
        else:
            histories = None
        return Response({'history': histories})
    elif request.method == 'POST':
        storage_id = request.POST.get('storage_id')
        try:
            storage = Storage.objects.get(pk=storage_id)
        except Storage.DoesNotExist:
            return Response({"info": "图书不存在"})
        remain = storage.remain
        if remain > 0:
            storage.remain = remain - 1
            storage.save()
            History(book=storage, user=request.user).save()
            return Response({"info": "借阅成功，等待审核!"})
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
        else:
            if history.user == request.user and status_old == 2:
                history.status = 4
        history.save()
        return Response({"status": history.status})
    elif request.method == 'GET':
        histories = History.objects.filter(pk=pk, user=request.user)
        if histories:
            serializer = HistorySerializer(histories, many=True)
            histories = serializer.data
        else:
            histories = None
        return Response({'history': histories})




