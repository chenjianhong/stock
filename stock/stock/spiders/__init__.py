#coding:utf-8
import json
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import Spider
from scrapy.http import Request
from stock.items import ListedCompany

class ListedCompanySpider(Spider):
    name = "sina_listed_company"
    start_urls = (
            'http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[["hq","hs_a","",0,1,100]]',
    )

    def __init__(self, name=None, **kwargs):
        super(ListedCompanySpider, self).__init__( name=None, **kwargs)
        self.listed_company_count = 0

    def parse(self,response):
        base_url = 'http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[["hq","hs_a","",0,%s,100]]'
        json_response = json.loads(response.xpath('//pre/text()').extract()[0])
        company_count = json_response[0]['count']
        page_count = company_count/100
        for page in range(0,page_count+2):
            next_link = base_url%page
            yield Request(url=next_link, callback=self.parse_detail)

    def parse_detail(self,response):
        json_response = json.loads(response.xpath('//pre/text()').extract()[0])
        print self.listed_company_count
        for company_data in json_response[0]['items']:
            self.listed_company_count += 1
            listed_company = ListedCompany()
            listed_company['symbol'] = company_data[0]
            listed_company['code'] = company_data[1]
            listed_company['name'] = company_data[2]
            yield listed_company
