# 引入path
from django.urls import path
# 引入views.py
from . import views
# 正在部署的应用的名称
app_name = 'ChatGPT_collector'

urlpatterns = [
    # 目前还没有urls
    path('ChatGPT_collector_page/', views.request_page, name='ChatGPT_collector_page'),
    path('request-create/', views.request_create, name='request_create'),
]