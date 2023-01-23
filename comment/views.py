from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from article.models import ArticlePost
from .forms import CommentForm
from .models import Comment
from notifications.signals import notify
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='/userprofile/login/')
# 新增参数 parent_comment_id
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=article_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                #MPTT的get_root()方法将其父级重置为树形结构最底部的一级评论，然后在reply_to中保存实际的被回复人并保存。
                #视图最终返回的是HttpResponse字符串
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                # 新增代码，给其他用户发送通知(除了superuser以外。用户之间可以互相评论，因此需要发送通知。if语句是为了防止管理员收到重复的通知。)
                if not parent_comment.user.is_superuser:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回复了你',
                        target=article,
                        action_object=new_comment,
                    )
                return HttpResponse('200 OK')
            new_comment.save()
            # 新增代码，给管理员发送通知（普通用户回复时给管理员发送通知。）
            if not request.user.is_superuser:
                notify.send(
                    request.user,
                    recipient=User.objects.filter(is_superuser=1),
                    verb='回复了你',
                    target=article,
                    action_object=new_comment,
                )
            return redirect(article)
        else:
            return HttpResponse('评论表单内容有误，请重新填写')
    elif request.method == 'GET':
        #新增处理GET请求的逻辑，用于给二级回复提供空白的表单。后面会用到。
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
        #多级评论使用了iframe？这是HTML5中的新特性，可以理解成当前网页中嵌套的另一个独立的网页。
        # 既然是独立的网页，那自然也会独立的向后台请求数据。
        # 仔细看src中请求的位置，正是前面我们在urls.py中写好的第二个path。即对应了post_comment视图中的GET逻辑：
    else:
        return HttpResponse('评论仅接受GET/POST请求')
