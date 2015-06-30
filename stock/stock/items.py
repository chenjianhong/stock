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
    smallest = scrapy.Field()
    small= scrapy.Field()
    bigger = scrapy.Field()
    biggest = scrapy.Field()


class Token(scrapy.Item):
    type = scrapy.Field()
    token = scrapy.Field()
    token_date = scrapy.Field()
