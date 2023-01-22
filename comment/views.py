from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from article.models import ArticlePost
from .forms import CommentForm

# Create your views here.
@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id):
    article = get_object_or_404(ArticlePost, id=article_id)
    # get_object_or_404()：它和Model.objects.get()的功能基本是相同的。
    # 区别是在生产环境下，如果用户请求一个不存在的对象时，
    # Model.objects.get()会返回Error500（服务器内部错误）
    # 而get_object_or_404()会返回Error
    # 404。相比之下，返回404错误更加的准确。
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            return redirect(article)
            # redirect()：返回到一个适当的url中：即用户发送评论后，重新定向到文章详情页面。
            # 当其参数是一个Model对象时，会自动调用这个Model对象的get_absolute_url()
            # 方法。因此接下来马上修改article的模型。
        else:
            return HttpResponse('评论表单内容有误，请重新填写')
    else:
        return HttpResponse('评论仅接受POST请求')
