from django.contrib import admin

# Register your models here.

# Register your models here.

# 别忘了导入ArticlerPost
from .models import ChatGPT3RequestorModel

# ChatGPTRequestorModel
admin.site.register(ChatGPT3RequestorModel)