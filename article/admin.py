from django.contrib import admin
#“告诉”Django，后台中需要添加ArticlePost这个数据表供管理

# Register your models here.
# 别忘了导入ArticlerPost
from .models import ArticlePost
# 注册ArticlePost到admin中
admin.site.register(ArticlePost)
from .models import ArticleColumn
admin.site.register(ArticleColumn)