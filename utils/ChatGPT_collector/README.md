# ChatGPT_collector

基于Python和MongoDB的ChatGPT问答数据采集程序 

## 程序执行流程：

1. 把input.txt中的问题存储到MongoDB的input集合中
2. 从MongoDB的input集合中读取问题，基于协程对openaiAPI接口进行异步访问，得到问题的回答
3. 将得到的回答进行处理，生成回答文档，并存入MongoDB的output集合中

## 说明
1. 问题存储在input.txt中，每个问题以逗号分隔
2. 程序默认请求OpenAI模型中耗时较久但回答质量较高的text-davinci-003，一次运行收集示例中的四个问题的问答数据
3. 为保证返回结果完整，设置了回答的长度限制limit_answer，对原始的问题进行长度限制，避免输出无意义的结果
4. 如果需要快速多次测试，可以修改ChatGPT_collector.py中的`engine="text-davinci-003"`，将engine换成开销更小的text-curie-001、text-babbage-001或text-ada-001

## 使用步骤：
1. 安装所需依赖包： 在项目根目录，用命令行运行以下代码：`pip install -r requirements.txt`
2. 设置api接口：将ChatGPT_collector.py里的openai.api_key换成自己OpenAI账号的api_key
3. 运行程序：在项目根目录，用命令行运行以下代码：`python .\ChatGPT_collector.py`