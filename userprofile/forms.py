# 13.用户的登录和退出
from django import forms
from django.contrib.auth.models import User
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
