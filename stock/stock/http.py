from scrapy.http import Request, TextResponse
__author__ = 'chenjianhong'


class PhantomJSRequest(Request):
    """A Request needed when using the phantomjs download handler."""
    WAITING = None

    def __init__(self, url, manager=None, **kwargs):
        super(PhantomJSRequest, self).__init__(url, **kwargs)
        self.manager = manager

    def replace(self, *args, **kwargs):
        kwargs.setdefault('manager', self.manager)
        return super(PhantomJSRequest, self).replace(*args, **kwargs)
