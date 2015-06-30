# -*- coding: utf-8 -*-

# Scrapy settings for stock project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'stock'

LOG_FILE = "logs/scrapy.log"

SPIDER_MODULES = ['stock.spiders']
NEWSPIDER_MODULE = 'stock.spiders'

ITEM_PIPELINES = {
    # 'stock.pipelines.ListedCompanyPipeline': 1,
    'stock.pipelines.fund.TokenPipeline': 1,
    'stock.pipelines.fund.FundPipeline': 2
}

# DOWNLOADER_MIDDLEWARES = {
#     'stock.contrib.downloadmiddleware.phantomjs.JsDownload': 1,
# }

DOWNLOAD_HANDLERS = {
    'http': 'stock.contrib.downloader.phantomjs.PhantomJSDownloadHandler'
}

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'fund'