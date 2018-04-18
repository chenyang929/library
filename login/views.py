from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def login_view(request):
    link = '/library/'
    if request.user.is_authenticated:
        if request.user.is_superuser:
            link = '/library/backend/'
        return redirect(link)
    else:
        context = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    link = '/library/backend/'
                return redirect(link)
            else:
                context.update({'error_message': '用户名、邮箱或密码错误，请重新登录'})
        return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login:login')
