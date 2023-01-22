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
class ContextMixin:
    '''
    混入类（Mixin）是指具有某些功能、通常不独立使用、提供给其他类继承功能的类。嗯，就是“混入”的字面意思。
    '''
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
    context_object_name = 'articles'
    template_name = 'article/list.html'
    def get_queryset(self):
        """
        查询集
        """
        queryset = ArticlePost.objects.filter(title='Python')
        return queryset


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

class ArticleCreateView(CreateView):
    model = ArticlePost
    fields = '__all__'
    template_name = 'article/create_by_class_view.html'

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

