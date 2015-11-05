#coding:utf-8
import re
import json
import datetime

from scrapy.spider import Spider
from scrapy.http import Request
from scrapy import log
from pymongo import MongoClient

from stock.models.items import ListedCompany,Token


class TokenSpider(Spider):
    name = "token"
    start_urls = (
            'http://hqres.eastmoney.com/EMQuote_Center2.0/js/list.min.js',
    )

    def parse(self,response):
        search_result = re.search('"&token=([0-9a-z]{32})"',response.body_as_unicode())
        if search_result:
            token = search_result.groups()[0]
            token_item = Token()
            token_item['type'] = self.name
            token_item['token'] = token
            token_item['token_date'] = datetime.datetime.now().strftime('%Y%m%d')
            yield token_item
        else:
            log.err('token get error!')
            yield None


class ListedCompanySpider(Spider):

    name = "company"

    base_url = 'http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/index.aspx?type=s&sortType=C&sortRule=-1&pageSize=500&page=%s&style=33&token=%s'

    # start_urls = (
    #         'http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[["hq","hs_a","",0,1,100]]',
    #         'http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/index.aspx?type=s&sortType=C&sortRule=-1&pageSize=20&page=1&style=33&token=44c9d251add88e27b65ed86506f6e5da'
    # )

    def __init__(self, name=None, **kwargs):
        super(ListedCompanySpider, self).__init__( name=None, **kwargs)
        self.listed_company_count = 0


    def close_spider(self,spider):
        self.client.close()

    @classmethod
    def from_crawler(cls, crawler):
        cls.MONGODB_SERVER = crawler.settings.get('MONGODB_SERVER')
        cls.MONGODB_PORT = crawler.settings.getint('MONGODB_PORT')
        cls.MONGODB_DB = crawler.settings.get('MONGODB_DB')
        pipe = cls()
        return pipe

    def start_requests(self):
        self.client = MongoClient(self.MONGODB_SERVER,self.MONGODB_PORT)
        self.db = self.client[self.MONGODB_DB]
        token_date = datetime.datetime.now().strftime('%Y%m%d')
        self.token =self.db['token'].find_one({'token_date':token_date})
        first_page = self.base_url%(1,self.token)
        return [Request(url=first_page, callback=self.parse)]

    def parse(self,response):
        data = response.body_as_unicode()[7:]
        data = data.replace('pages','"pages"')
        data = data.replace('rank','"rank"')
        json_response = json.loads(data)
        page_count = json_response['pages']
        for page in range(1,page_count+1):
            next_link = self.base_url%(page,self.token)
            yield Request(url=next_link, callback=self.parse_detail)

    def parse_detail(self,response):
        data = response.body_as_unicode()[7:]
        data = data.replace('pages','"pages"')
        data = data.replace('rank','"rank"')
        json_response = json.loads(data)
        for company_data in json_response['rank'][:2]:
            self.listed_company_count += 1
            print company_data
            listed_company = ListedCompany()
            listed_company['symbol'] = company_data[0]
            listed_company['code'] = company_data[1]
            listed_company['name'] = company_data[2]
            print company_data
            yield listed_company




class CompanyDetailSpider(Spider):
    name = "company_detail"

    def __init__(self, name=None, **kwargs):
        super(CompanyDetailSpider, self).__init__( name=None, **kwargs)
        self.listed_company_count = 0

    def start_requests(self):
        base_url = 'http://finance.sina.com.cn/realstock/company/sh600004/nc.shtml'
        return [Request(url=base_url, callback=self.parse)]

    def parse(self,response):
        for i in response.xpath('//div[@id="FLFlow"]/table/tbody/tr[2]/td/text()').extract():
            print i
        return None

    def parse_detail(self,response):
        json_response = json.loads(response.body_as_unicode())
        for company_data in json_response[0]['items']:
            self.listed_company_count += 1
            listed_company = ListedCompany()
            listed_company['symbol'] = company_data[0]
            listed_company['code'] = company_data[1]
            listed_company['name'] = company_data[2]
            yield listed_company
