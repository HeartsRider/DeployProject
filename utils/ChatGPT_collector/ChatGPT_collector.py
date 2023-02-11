import openai
import asyncio
import aiohttp
import time
import pymongo
import datetime
import hashlib


def db_init():
    """数据库连接与初始化"""
    my_client = pymongo.MongoClient("mongodb://tyliu:tyl_pw7081@39.101.132.159:27019/test_chatgpt4ty?authMechanism=DEFAULT&authSource=test_chatgpt4ty")
    my_db = my_client["test_chatgpt4ty"]
    collection_input = my_db["input"]
    collection_output = my_db["output"]
    return collection_input, collection_output


def store_queries(collection_input, filename):
    """从filename文件中读取问题，并存入MongoDB问题集合collection_input中"""
    with open(filename, "r", encoding='utf-8') as f:
        input_data = f.read()
    input_queries = input_data.split(',')
    for query in input_queries:
        input_document = {'md5_val': hashlib.md5(query.encode('utf-8')).hexdigest(), 'payload': query}
        collection_input.insert_one(input_document)


def read_queries(collection_input):
    """从MongoDB问题集合collection_input中读取所有问题，储存在列表中queries中并返回"""
    queries = []
    for item in collection_input.find():
        queries.append(item['payload'])
    return queries


async def get_response(input_query):
    """异步访问openai接口，返回所得到的响应response"""
    time.sleep(3)
    openai.aiosession.set(aiohttp.ClientSession())
    response = await openai.Completion.acreate(
        engine="text-davinci-003",
        prompt=input_query,
        temperature=0.5,
        max_tokens=2000,
        n=1
    )
    await openai.aiosession.get().close()
    return response


def update_collection(collection_output, doc):
    """用新产生的文档doc更新MongoDB的output集合"""
    query_condition = {'input_md5': doc['input_md5']}  # 用输入问题md5值，查询集合中是否已存在该问题的回答文档
    answer_condition = {'results.answer_md5': doc['results'][0]['answer_md5']}  # 用新回答的md5值，确定文档中是否已存在相同内容的回答

    # 如果不存在这个问题的回答文档，那么将新文档作为最终文档插入集合
    if not collection_output.find_one(query_condition):
        updated_doc = doc

    # 如果存在这个问题的回答文档，那么更新原有的文档，得到最终文档
    else:
        doc_with_same_answer = collection_output.find_one(answer_condition)

        # 如果数据库中不存在相同的回答，则将此回答插入到对应问题下results文档数组的第0项
        if not doc_with_same_answer:
            doc_with_same_query = collection_output.find_one(query_condition)
            doc_with_same_query['results'].insert(0, doc['results'][0])
            updated_doc = doc_with_same_query

        # 如果数据库中已存在相同的回答，用更新原回答的last_compared_time
        else:
            for result in doc_with_same_answer['results']:
                if result['answer_md5'] == doc['results'][0]['answer_md5']:
                    result['last_compared_time'] = doc['results'][0]['last_compared_time']
            updated_doc = doc_with_same_answer

    # 用最终确定的文档进行更新/插入
    collection_output.update_one(query_condition, {'$set': updated_doc}, upsert=True)


async def collect_answer(collection_output, query, limit_answer):
    """异步地发起对于问题query的请求，回答由limit_answer控制长度，按照业务需求生成新文档new_doc，使用新文档更新output集合"""
    prompt = "请用最多" + str(limit_answer) + "个字回答：" + query
    response = await get_response(prompt)
    print("问题：", query, "\n回答：", response["choices"][0]["text"], '\n')
    new_doc = {
        'input_payload': query,
        'input_md5': hashlib.md5(query.encode('utf-8')).hexdigest(),  # 存储该问题的md5值，方便查询重复问题
        'prompt': prompt,
        'results': [
            {
                'answer': response["choices"][0]["text"],
                'created_time': datetime.datetime.now(),
                'last_compared_time': datetime.datetime.now(),
                'answer_md5': hashlib.md5(response["choices"][0]["text"].encode('utf-8')).hexdigest()  # 存储该回答的md5值，方便确定重复回答
            }
        ]
    }
    update_collection(collection_output, new_doc)


if __name__ == '__main__':
    start_time = time.time()
    openai.api_key = "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"  # 设置自己的api
    my_input, my_output = db_init()
    if my_input.count_documents({}) == 0:
        store_queries(my_input, 'input.txt')
    tasks = [asyncio.ensure_future(collect_answer(my_output, query, limit_answer=100)) for query in read_queries(my_input)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    end_time = time.time()
    print('Cost time:', end_time - start_time)


