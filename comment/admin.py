from django.contrib import admin

# Register your models here.
#为方便测试，修改comment/admin.py文件，将评论模块注册到后台中：
from .models import Comment
admin.site.register(Comment)