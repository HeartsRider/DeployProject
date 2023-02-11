from django.contrib import admin

# Register your models here.

# 别忘了导入ArticlerPost
from .models import ChatGPTRequestorModel

# ChatGPTRequestorModel
admin.site.register(ChatGPTRequestorModel)