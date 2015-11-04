#coding:utf-8
import json
import re
from scrapy.spider import Spider
from scrapy.http import Request

class MainFund(Spider):
    name = "fund"
    fund_urls = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/MoneyFlow.ssl_qsfx_lscjfb?page=1&num=%s&sort=opendate&asc=0&daima=%s'
    page_number = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/MoneyFlow.ssc_qsfx_lscjfb?daima=%s'
    company_code = 'sh600664'

    def __init__(self, name=None, **kwargs):
        super(MainFund, self).__init__( name=None, **kwargs)
        self.listed_company_count = 0

    def start_requests(self):
        index_url = self.page_number%self.company_code
        return [Request(url=index_url, callback=self.parse)]

    def parse(self,response):
        page_count = re.search(r"[0-9]+",response.body_as_unicode())
        if page_count:
            print page_count.group()
            yield Request(url=self.fund_urls%(page_count.group(),self.company_code), callback=self.parse_detail)

    def parse_detail(self,response):
        json_response = json.loads(re.sub(r"([,{])(\w+):", "\\1\"\\2\" :", response.body_as_unicode()))
        for fund_data in json_response:
            yield []



