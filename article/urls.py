# 引入path
from django.urls import path
from . import  views

# 正在部署的应用的名称
app_name = 'article'

urlpatterns = [
    #path('article-list/', old_views.article_list, name ='article_list'),
    #<int:id>：Django2.0的path新语法用**尖括号<>**定义需要传递的参数。
    # 这里需要传递名叫id的整数到视图函数中去。
    # 就是把url里面article-detail/x/的x传给了view函数
    path('article-list/', views.ArticleListView.as_view(), name='article_list'),
    path('article-detail/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    # path(route, view, kwargs=None, name=None)
    #The view argument is a view function or the result of as_view() for class-based views.
    # It can also be an django.urls.include().
    #path('article-delete/<int:id>/', views.article_delete, name = 'article_delete'),
    path('article-safe-delete/<int:id>/', views.article_safe_delete, name ='article_safe_delete'),
    path('article-create/', views.ArticleCreateView.as_view(), name ='article_create'),
    path('article-update/<int:id>/', views.article_update, name ='article_update'),
]