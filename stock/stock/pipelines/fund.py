# -*- coding: utf-8 -*-
from pymongo import MongoClient, TEXT


class FundPipeline(object):

    collection_name = 'fund'

    def open_spider(self,spider):
        self.client = MongoClient(self.MONGODB_SERVER,self.MONGODB_PORT)
        self.db = self.client[self.MONGODB_DB]

    def close_spider(self,spider):
        self.client.close()

    @classmethod
    def from_crawler(cls, crawler):
        cls.MONGODB_SERVER = crawler.settings.get('MONGODB_SERVER')
        cls.MONGODB_PORT = crawler.settings.getint('MONGODB_PORT')
        cls.MONGODB_DB = crawler.settings.get('MONGODB_DB')
        pipe = cls()
        return pipe

    def process_item(self,item,spider):
        self.db[self.collection_name].insert(dict({'test':1}))
        return item

class TokenPipeline(object):

    collection_name = 'token'


    def open_spider(self,spider):
        self.client = MongoClient(self.MONGODB_SERVER,self.MONGODB_PORT)
        self.db = self.client[self.MONGODB_DB]
        self.db[self.collection_name].create_index([('token_date',TEXT)],name='index_1',unique=True)

    def close_spider(self,spider):
        self.client.close()

    @classmethod
    def from_crawler(cls, crawler):
        cls.MONGODB_SERVER = crawler.settings.get('MONGODB_SERVER')
        cls.MONGODB_PORT = crawler.settings.getint('MONGODB_PORT')
        cls.MONGODB_DB = crawler.settings.get('MONGODB_DB')
        pipe = cls()
        return pipe

    def process_item(self,item,spider):
        if item['type'] == 'token':

            self.db[self.collection_name].update({'token_date':item['token_date']},{'token':item['token'],'token_date':item['token_date']},upsert=True)
            return None
        else:
            return item