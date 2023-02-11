# Create your views here.
# 引入redirect重定向模块
from django.shortcuts import render, redirect
# 引入HttpResponse
from django.http import HttpResponse
# 引入刚才定义的ArticlePostForm表单类
from .forms import QueryPostForm
# 引入User模型
from django.contrib.auth.models import User

import openai

#payload = '使用SwiftUI写一个登陆界面'

# 导入数据模型
from .models import ChatGPT3RequestorModel


def process_data(input, key):
    openai.api_key = key
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=input,
        temperature=0.9,
        max_tokens=2000,
        top_p=1.0,
    )
    answer = response.choices[0].text
    return answer


def request_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        request_post_form = QueryPostForm(request.POST)
        # 判断提交的数据是否满足模型的要求
        if request_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_query = request_post_form.save(commit=False)
            payload = request_post_form.cleaned_data['payload']
            key = request_post_form.cleaned_data['apikey']
            answer  = process_data(payload, key)
            # 将新文章保存到数据库中
            new_query.save()
            # 完成后返回到文章列表
            return render(request, 'ChatGPT_collector/ShowResults.html', {'answer': answer, 'payload': payload})
            #return redirect("ChatGPT_collector:ChatGPT_collector_page")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        request_post_form = QueryPostForm()
        # 赋值上下文
        context = {'QueryPostForm': QueryPostForm}
        # 返回模板
        return render(request, 'ChatGPT_collector/create.html', context)