from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
#因为模型中的2个外键(article,user)将通过视图逻辑自动填写，所以这里只需要提交body就足够了。