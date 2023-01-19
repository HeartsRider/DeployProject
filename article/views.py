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
# 引入User模型
from django.contrib.auth.models import User

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

#article_detail(request, id)函数中多了id这个参数。**注意我们在写model的时候并没有写叫做id的字段，
# **这是Django自动生成的用于索引数据表的主键（Primary Key，即pk）。
# 有了它才有办法知道到底应该取出哪篇文章。
def article_detail(request, id):
    #意思是在所有文章中，取出id值相符合的唯一的一篇文章。
    article = ArticlePost.objects.get(id = id)
    # 将markdown语法渲染成html样式,将Markdown语法书写的文章渲染为HTML文本
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                     ])
    context = {'article':article}
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
        # 调用.delete()方法删除文章
        article.delete()
        # 完成删除后返回文章列表,第一个article是app名字
        # 第二个article_list是在urls里面我们定义的名字
        return redirect("article:article_list")
    else:
        return HttpResponse('POST request only!')

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

def article_update(request, id):
    """
        更新文章的视图函数
        通过POST方法提交表单，更新titile、body字段
        GET方法进入初始表单页面
        id： 文章的 id
    """
    article = ArticlePost.objects.get(id=id)
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
