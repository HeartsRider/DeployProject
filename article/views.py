from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .models import ArticlePost
# 引入markdown模块
import markdown
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
from django.contrib.auth.decorators import login_required
# 引入User模型
from django.contrib.auth.models import User
# 引入分页模块
from django.core.paginator import Paginator
# 引入 Q 对象
from django.db.models import Q
from comment.models import Comment
'''
def article_list(request):
    #ArticlePost.objects.all()是数据类的方法，可以获得所有的对象（即博客文章），并传递给articles变量
    articles = ArticlePost.objects.all() 
    
    #context定义了需要传递给模板的上下文，这里即articles
    context = {'articles': articles}
    #render函数的作用是结合模板和上下文，并返回渲染后的HttpResponse对象。
    #通俗的讲就是把context的内容，加载进模板，并通过浏览器呈现。
    # equest是固定的request对象，照着写就可以
    # article / list.html定义了模板文件的位置、名称
    # context定义了需要传入模板文件的上下文
    return render(request, 'article/list.html', context)
'''

# Chap 19.添加了分页功能的文章列表
def article_list(request):
    '''
    前面已经用到了将参数传递给views的两种方法：
        1. 通过POST请求将表单数据传递到视图
        2. 通过url将地址中的参数传递到视图
    这里用到的是：
        在GET请求中，在url的末尾附上?key=value的键值对，
        视图中就可以通过request.GET.get('key')来查询value的值。
        在视图中通过Paginator类，给传递给模板的内容做了手脚：
        返回的不再是所有文章的集合，而是对应页码的部分文章的对象，并且这个对象还包含了分页的方法。
    '''
    # 修改变量名称（articles -> article_list）
    order = request.GET.get('order')
    search = request.GET.get('search')
    if search:
        if order == 'total_views':
            article_list = ArticlePost.objects.filter(
                #在模型的title字段查询，icontains是不区分大小写的包含
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                #多个Q对象用管道符|隔开，就达到了联合查询的目的。
                Q(body__icontains=search)
            )
    else:
        search = ''
        #为什么要search = ''语句？如果用户没有搜索操作，则search = request.GET.get('search')
        # 会使得search = None，而这个值传递到模板中会错误地转换成"None"字符串！
        # 等同于用户在搜索“None”关键字，
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
            order = 'total_views'
        else:
            article_list = ArticlePost.objects.all()
            order = 'normal'
    # 每页显示 3 篇文章
    paginator = Paginator(article_list, 3)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    context = { 'articles': articles, 'order': order}
    return render(request, 'article/list.html', context)




#article_detail(request, id)函数中多了id这个参数。
# **注意我们在写model的时候并没有写叫做id的字段，
# **这是Django自动生成的用于索引数据表的主键（Primary Key，即pk）。
# 有了它才有办法知道到底应该取出哪篇文章。
def article_detail(request, id):
    #意思是在所有文章中，取出id值相符合的唯一的一篇文章。
    article = ArticlePost.objects.get(id = id)
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # 将markdown语法渲染成html样式,将Markdown语法书写的文章渲染为HTML文本
    md = markdown.Markdown(
                         extensions=[
                             # 包含 缩写、表格等常用扩展
                             'markdown.extensions.extra',
                             # 语法高亮扩展
                             'markdown.extensions.codehilite',
                             #目录扩展
                             'markdown.extensions.toc',
                         ])

    comments = Comment.objects.filter(article=id)
    article.body = md.convert(article.body)
    context = {'article': article, 'toc': md.toc, 'comments': comments}
    return render(request, 'article/detail.html', context)

def article_delete(request, id):
    # 意思是在所有文章中，取出id值相符合的唯一的一篇文章。
    article = ArticlePost.objects.get(id=id)
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表,第一个article是app名字
    # 第二个article_list是在urls里面我们定义的名字
    return redirect("article:article_list")

def article_safe_delete(request, id):
    '''
    描述：带csrf验证的安全删除函数
    没发现哪行代码校验了csrf令牌啊？
    放心，默认配置下所有的 POST 请求都由 Django 中间件帮你验证了。
    另外视图一定要限制为 POST 请求，
    即if request.method == 'POST'必须有，就请读者思考一下原因吧。

    凡是重要的数据操作，都应该考虑带有 csrf 令牌的 POST 请求；
    简单记忆的原则，数据查询用 GET，数据更改用 POST。
    '''
    if request.method == 'POST':
        # 意思是在所有文章中，取出id值相符合的唯一的一篇文章。
        article = ArticlePost.objects.get(id=id)
        if request.user != article.author:
            return HttpResponse('抱歉，你无权删除这篇文章')
        # 调用.delete()方法删除文章
        article.delete()
        # 完成删除后返回文章列表,第一个article是app名字
        # 第二个article_list是在urls里面我们定义的名字
        return redirect("article:article_list")
    else:
        return HttpResponse('POST request only!')
'''
#profile修改之前的article_create:
#两点问题:  1. new_article.author = User.objects.get(id=1)强行把作者指定为id=1的用户，这显然是不对的。
          2. 没有对用户的登录状态进行检查。
#解决:     1. User.objects.get(id=request.user.id)
          2. 添加装饰器login_required
def article_create(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse('invalid form, please imput again!')
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form':article_post_form}
        return render(request, 'article/create.html', context)
'''

@login_required(login_url='/userprofile/login/')
def article_create(request):

    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            #new_article.author = User.objects.get(id=1)
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse('invalid form, please imput again!')
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form': article_post_form}
        return render(request, 'article/create.html', context)

def article_update(request, id):
    """
        更新文章的视图函数
        通过POST方法提交表单，更新titile、body字段
        GET方法进入初始表单页面
        id： 文章的 id
    """
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse('抱歉，你无权修改这篇文章')
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect('article:article_detail', id=id)
        else:
            return HttpResponse('invalid form, please input again!')
    else:
        article_post_form = ArticlePostForm()
        context = { 'article': article, 'article_post_form': article_post_form }
        return render(request, 'article/update.html', context)

