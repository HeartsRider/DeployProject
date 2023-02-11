import pymongo

def db_init():
    """数据库连接与初始化"""
    my_client = pymongo.MongoClient("mongodb://localhost:27017")
    my_db = my_client["blog_chatGPT_db"]
    collection_input = my_db["input"]
    collection_output = my_db["output"]
    return collection_input, collection_output
if __name__ == '__main__':
    input_db, result_db = db_init()
    print(input_db)
    print(result_db)

