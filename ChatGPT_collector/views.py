from django.shortcuts import render

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
#openai.api_key = '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'
#payload = '使用SwiftUI写一个登陆界面'

# 导入数据模型
from .models import ChatGPTRequestorModel

def request_page(request):
    #collection = ChatGPTRequestorModel.objects.using('mongo').all()
    #payload = ChatGPTRequestorModel.object.all()
    payload = request.GET.get('payload')
    api_key = request.GET.get('apikey')

    # 需要传递给模板（templates）的对象
    answer = process_data(payload, api_key)
    # render函数：载入模板，并返回context对象
    return render(request, 'ChatGPT_collector/ShowResults.html', {'answer': answer, 'payload': payload})


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


# def process_input(request):
#     if request.method == 'POST':
#         input_data = request.POST.get('input_field')
#         # Do something with the input data
#         processed_data = process_data(input_data)
#         # Save the processed data
#         input_instance = InputData.objects.create(input_field=processed_data)
#         return redirect('some_view_name')
#     else:
#         return render(request, 'input_form.html')


def request_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        request_post_form = QueryPostForm(request.POST)
        # 判断提交的数据是否满足模型的要求
        if QueryPostForm.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_query = QueryPostForm.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            # 将新文章保存到数据库中
            new_query.save()
            # 完成后返回到文章列表
            return redirect("ChatGPT_collector:ChatGPT_collector_page")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = QueryPostForm()
        # 赋值上下文
        context = {'QueryPostForm': QueryPostForm}
        # 返回模板
        return render(request, 'ChatGPT_collector/create.html', context)