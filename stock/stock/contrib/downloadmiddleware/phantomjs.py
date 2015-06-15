#coding:utf-8
from scrapy import log
from scrapy.http import HtmlResponse
from selenium import webdriver

__author__ = 'mason'

class JsDownload(object):

    def process_request(self, request, spider):
        # if request.meta.has_key('PhantomJS'):# 如果设置了PhantomJS参数，才执行下面的代码
            log.msg('PhantomJS Requesting: '+request.url, level=log.WARNING)
            service_args = ['--load-images=false', '--disk-cache=true']
            if request.meta.has_key('proxy'): # 如果设置了代理(由代理中间件设置)
                log.msg('PhantomJS proxy:'+request.meta['proxy'][7:], level=log.WARNING)
                service_args.append('--proxy='+request.meta['proxy'][7:])
            try:
                driver = webdriver.PhantomJS(service_args = service_args)
                driver.get(request.url)
                content = driver.page_source.encode('utf-8')
                url = driver.current_url.encode('utf-8')
                driver.quit()
                if content == '<html><head></head><body></body></html>':# 内容为空，当成503错误。交给重试中间件处理
                    return HtmlResponse(request.url, encoding = 'utf-8', status = 503, body = '')
                else: # 返回response对象
                    return HtmlResponse(url, encoding = 'utf-8', status = 200, body = content)
            except Exception, e: # 请求异常，当成500错误。交给重试中间件处理
                log.msg('PhantomJS Exception!', level=log.WARNING)
                return HtmlResponse(request.url, encoding = 'utf-8', status = 503, body = '')
        # else:
        #     log.msg('Common Requesting: '+request.url, level=log.WARNING)