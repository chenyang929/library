from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, History
from .serializers import BookSerializer, HistorySerializer
from django.shortcuts import render
from django.contrib.auth.models import User
import datetime


def index(request):
    context = {'visitor': request.user}
    return render(request, 'index.html', context)


def manage(request):
    context = {'visitor': request.user}
    return render(request, 'manage.html', context)


def get_start_end(page, per_page_num, count):
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


@api_view(['GET', ])
def book_list_api(request, page):
    page = int(page)
    books = Book.objects.all()
    if not books:
        return Response({"results": None})
    count = books.count()
    per_page_num = 15
    mp = get_start_end(page, per_page_num, count)
    start = mp['start']
    end = mp['end']
    previous_page = mp['previous_page']
    next_page = mp['next_page']
    books_per = books[start:end]
    serializer = BookSerializer(books_per, many=True)
    mp = {"counts": count, "results": serializer.data, "next_page": next_page, "previous_page": previous_page}
    return Response(mp)


@api_view(['GET', ])
def book_list_filter_api(request, status, page):
    if int(status) > 1:
        status = 1
    page = int(page)
    books = Book.objects.filter(remain=status)
    if not books:
        return Response({"results": None})
    count = books.count()
    per_page_num = 15
    mp = get_start_end(page, per_page_num, count)
    start = mp['start']
    end = mp['end']
    previous_page = mp['previous_page']
    next_page = mp['next_page']
    books_per = books[start:end]
    serializer = BookSerializer(books_per, many=True)
    mp = {"counts": count, "results": serializer.data, "next_page": next_page, "previous_page": previous_page}
    return Response(mp)


@api_view(['GET', ])
def book_detail_api(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = BookSerializer(book)
    return Response(serializer.data)


@api_view(['GET'])
def history_list_api(request):
    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        return Response({'history': None})
    if request.user.username == 'admin':
        histories = History.objects.all()
    else:
        histories = History.objects.filter(user=user)
    if histories:
        serializer = HistorySerializer(histories, many=True)
        histories = serializer.data
    else:
        histories = None
    return Response({'history': histories})


@api_view(['GET', 'POST'])
def history_detail_api(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        history = History.objects.filter(book=pk)
        if history:
            serializer = HistorySerializer(history, many=True)
            history = []
            for ser in serializer.data:
                ser.pop('book')
                history.append(ser)
            return Response({'book': book.book, 'history': history})
        return Response({'book': book.book, 'history': None})
    elif request.method == 'POST':
        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            return Response({"message": "anonymous"})
        book_remain = book.remain
        if book_remain > 0:
            book.remain = book_remain-1
            book.save()
            History(book=book, user=user).save()
            return Response({"message": "借阅成功，等待审核!"})
        else:
            return Response({"message": "ops!手慢了"})


@api_view(['POST'])
def book_back(request, pk):
    user = User.objects.get(username=request.user)
    try:
        history = History.objects.get(pk=pk, user=user)
    except History.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if history.status == 1:
        history.status = 3
        history.save()
        return Response({"message": "等待管理员确认"})
    else:
        return Response({"message": "无效操作"})


@api_view(['POST'])
def check(request, pk):
    if request.user.username != 'admin':   # 改写装饰器
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        history = History.objects.get(pk=pk)
    except History.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    history_status = history.status
    info = request.POST.get('info')
    if info:
        if info == 'agree':
            if history_status == 2:
                history.status = 1
                history.save()
            elif history_status == 3:
                history.status = 0
                history.back_date = datetime.date.today()
                history.save()
                book = Book.objects.get(pk=history.book_id)
                remain = book.remain
                book.remain = remain + 1
                book.save()
        elif info == 'disagree':
            if history_status == 2:
                history.status = 4
                history.save()
                book = Book.objects.get(pk=history.book_id)
                remain = book.remain
                book.remain = remain + 1
                book.save()
            elif history_status == 3:
                pass
    return Response({"info": info})


@api_view(['POST'])
def book_add(request):
    if request.user.username != 'admin':
        return Response(status=status.HTTP_403_FORBIDDEN)
    title = request.POST.get("book")
    if title and not Book.objects.filter(book=title):
        Book.objects.create(book=title)
        info = '图书入库成功!'
    else:
        info = '图书已存在!'
    return Response({"info": info})
