from django.db import models
from django.contrib.auth.models import User
from article.models import ArticlePost
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
# Create your models here.
class Comment(MPTTModel):
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    # 之前为 body = models.TextField()
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    # 新增，mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    # 新增，记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )
    # 替换 Meta 为 MPTTMeta
    # class Meta:
    #     ordering = ('created',)
    class MPTTMeta:
        order_insertion_by = ['created']
    def __str__(self):
        return self.body[:20]
