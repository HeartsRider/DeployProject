from django.urls import path
from . import views
app_name = 'comment'
urlpatterns = [
    # 已有代码，处理一级回复
    path('post-comment/<int:article_id>', views.post_comment, name='post_comment'),
    # 新增代码，处理二级回复
    path('post-comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply'),
]
#两个path都使用了同一个视图函数，但是传入的参数却不一样多，仔细看。
# 第一个path没有parent_comment_id参数，因此视图就使用了缺省值None，达到了区分评论层级的目的。