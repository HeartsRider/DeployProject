# 13.用户的登录和退出
from django import forms
from django.contrib.auth.models import User
from .models import Profile
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

#对数据库进行操作的表单应该继承forms.ModelForm，可以自动生成模型中已有的字段。
# 注册用户表单
class UserRegisterForm(forms.ModelForm):
    # 复写 User 的密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致,请重试。")
        '''
        从POST中取值用的data.get('password')
        是一种稳妥的写法，即使用户没有输入密码也不会导致程序错误而跳出。
        前面章节提取POST数据我们用了data['password']，
        这种取值方式如果data中不包含password，Django会报错。
        '''
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')