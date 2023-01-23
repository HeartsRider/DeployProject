#基于类视图
# from django.shortcuts import render
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

from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from .models import ArticleColumn
from comment.forms import CommentForm
class ContextMixin:
    def get_context_data(self, **kwargs):
        # 获取原有的上下文
        context = super().get_context_data(**kwargs)
        # 增加新上下文
        context['order'] = 'total_views'
        return context

class ArticleListView(ContextMixin, ListView):
    #通过混入，两个子类都获得了get_context_data()方法。
    #从语法上看，混入是通过多重继承实现的。有区别的是，Mixin是作为功能添加到子类中的，而不是作为父类。
    #Django内置了很多通用的Mixin类，实现了大部分常用的功能，可以往官方文档进一步了解
    """处理GET请求"""
    def get(self, request):
        articles = ArticlePost.objects.all()
        context = {'articles': articles}
        return render(request, 'article/list.html', context)
    context_object_name = 'articles'
    template_name = 'article/list.html'
    def get_queryset(self):
        """
        查询集
        """
        queryset = ArticlePost.objects.filter(title='Python')
        return queryset


def article_list(request):
    # 从 url 中提取查询参数
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    # 初始化查询集
    article_list = ArticlePost.objects.all()

    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
    }

    return render(request, 'article/list.html', context)

class ArticleDetailView(DetailView):
    queryset = ArticlePost.objects.all()
    context_object_name = 'article'
    template_name = 'article/detail.html'
    def get_object(self):
        """
        获取需要展示的对象
        """
        # 首先调用父类的方法
        obj = super(ArticleDetailView, self).get_object()
        # 浏览量 +1
        obj.total_views += 1
        obj.save(update_fields=['total_views'])
        return obj

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
    # 引入评论表单
    comment_form = CommentForm()
    article.body = md.convert(article.body)
    context = {'article': article, 'toc': md.toc, 'comments': comments, 'comment_form':comment_form}
    return render(request, 'article/detail.html', context)

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

@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == 'POST':
        # 增加 request.FILES 为了文章的头像
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            #new_article.author = User.objects.get(id=1)
            new_article.author = User.objects.get(id=request.user.id)
            # 新增的代码
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            new_article.save()
            # 新增代码，保存 tags 的多对多关系
            article_post_form.save_m2m()
            return redirect("article:article_list")
        else:
            return HttpResponse('invalid form, please imput again!')
    else:
        article_post_form = ArticlePostForm()
        # 新增及修改的代码
        columns = ArticleColumn.objects.all()
        context = {'article_post_form': article_post_form, 'columns': columns}
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
            # 新增的代码
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            #处理文章头像更新，不能从请求的POST里获取，要从请求的FILE里获取
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            article.save()
            return redirect('article:article_detail', id=id)
        else:
            return HttpResponse('invalid form, please input again!')
    else:
        article_post_form = ArticlePostForm()
        # 新增及修改的代码
        columns = ArticleColumn.objects.all()
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
        }
        return render(request, 'article/update.html', context)

