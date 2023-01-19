# 引入表单类
from django import forms
# 引入文章模型
from .models import ArticlePost

# 写文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = ArticlePost
        # 定义表单包含的字段
        fields = ('title', 'body')
'''
代码中ArticlePostForm类继承了Django的表单类forms.ModelForm，
并在类中定义了内部类class Meta（之前提到过，还记得吗），
指明了数据模型的来源，以及表单中应该包含数据模型的哪些字段。

在ArticlePost模型中，created和updated字段为自动生成，不需要填入；
author字段暂时固定为id=1的管理员用户，也不用填入；
剩下的title和body就是表单需要填入的内容了。
'''