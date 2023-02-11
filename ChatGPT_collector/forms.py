# 引入表单类
from django import forms
# 引入文章模型
from .models import ChatGPTRequestorModel

# 写文章的表单类
class QueryPostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = ChatGPTRequestorModel
        # 定义表单包含的字段
        fields = ('apikey', 'payload')