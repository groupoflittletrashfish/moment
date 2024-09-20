from pymongo import MongoClient


class MongoSession:

    def __init__(self):
        # 创建 MongoClient 实例
        client = MongoClient('mongodb://139.224.163.144:27017/')
        self.session = client['noname']

    def get_mongo_session(self):
        return self.session
