# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ListedCompany(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    symbol = scrapy.Field()
    code = scrapy.Field()


class FundFlow(scrapy.Item):
    open_date = scrapy.Field()
    trade = scrapy.Field()
    changeratio = scrapy.Field()
    turnover = scrapy.Field()
    ratioamount = scrapy.Field()
    netamount = scrapy.Field()

    def get_text_output(self):
        return '\t'.join([self['open_date'],self['trade'],self['changeratio'],self['turnover'],self['ratioamount'],self['netamount']])


class Token(scrapy.Item):
    type = scrapy.Field()
    token = scrapy.Field()
    token_date = scrapy.Field()
