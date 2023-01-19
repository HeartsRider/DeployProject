from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm
# Create your views here.
#用户的登录是比较复杂的功能，好在Django提供了封装好的模块供我们使用。
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data = request.POST)
        # 跟发表文章的表单类类似，Form对象的主要任务就是验证数据。调用is_valid()
        # 方法验证并返回指定数据是否有效的布尔值。
        if user_login_form.is_valid():
            # Form不仅负责验证数据，还可以“清洗”它：将其标准化为一致的格式，
            # 这个特性使得它允许以各种方式输入特定字段的数据，并且始终产生一致的输出。
            # 一旦Form使用数据创建了一个实例并对其进行了验证，就可以通过cleaned_data属性访问清洗之后的数据。
            data = user_login_form.cleaned_data
            user = authenticate(username = data['username'], password = data['password'])
            if user:
                #login()方法实现用户登录，将用户数据保存在session中。
                # 什么是session
                # Session在网络应用中，称为 “会话控制”  ，
                # 它存储特定用户会话所需的属性及配置信息。
                # 当用户在Web页面之间跳转时，存储在Session对象中的变量将不会丢失，
                # 而是在整个用户会话中一直存在下去。
                # Session最常见的用法就是存储用户的登录数据。
                login(request, user)
                return redirect('article:article_list')
            else:
                return HttpResponse('Error in account or password! Please input again!')

        else:
            return HttpResponse('Invalid account or invalid password!')
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse('Please use GET or POST request!')

def user_logout(request):
    logout(request)
    return redirect('article:article_list')






