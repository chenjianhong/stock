#coding:utf-8
import json
from scrapy.spider import Spider
from scrapy.http import Request
from stock.items import ListedCompany

class MainFund(Spider):
    name = "fund"
    start_urls = (
            'http://data.eastmoney.com/zjlx/300468.html',
    )

    def __init__(self, name=None, **kwargs):
        super(MainFund, self).__init__( name=None, **kwargs)
        self.listed_company_count = 0

    def start_requests(self):
        base_url = 'http://data.eastmoney.com/zjlx/%s'
        return [Request(url=base_url, callback=self.parse)]

    def parse(self,response):
        base_url = 'http://data.eastmoney.com/zjlx/300468.html'
        json_response = json.loads(response.body_as_unicode())
        page_count = json_response['pages']
        for page in range(0,page_count+1):
            next_link = base_url%page
            yield Request(url=next_link, callback=self.parse_detail)

    def parse_detail(self,response):
        json_response = json.loads(response.body_as_unicode())
        for fund_data in json_response['data']:
            code = fund_data[1]
            main_fund = fund_data[5]
            main_fund_percent = fund_data[6]
            middle_fund = fund_data[11]
            middle_fund_percent = fund_data[12]
            little_fund = fund_data[13]
            littel_fund_percent = fund_data[14]
            if main_fund>0 and middle_fund<0 and little_fund<0:
                yield []



