from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile

# Create your views here.
#用户的登录是比较复杂的功能，好在Django提供了封装好的模块供我们使用。
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
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

# 用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = { 'form': user_register_form }
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

'''
@login_required是一个Python装饰器。
装饰器可以在不改变某个函数内容的前提下，给这个函数添加一些功能。
具体来说就是@login_required要求调用user_delete()函数时，用户必须登录；
如果未登录则不执行函数，将页面重定向到/userprofile/login/地址去。


'''
@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        if request.user == user:
            logout((request))
            user.delete()
            return redirect("article:article_list")
        else:
            return HttpResponse('你没有删除的权限')
    else:
        return HttpResponse('仅接受POST请求')

@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的字段
    profile = Profile.objects.get(user_id=id)

    if request.method == 'POST':
        if request.user != user:
            return HttpResponse("你没有修改此用户信息的权限。")
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]
            profile.save()
            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse('非法表单，请重新输入')
    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, 'profile':profile, 'user':user}
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse('请使用GET或POST请求数据')