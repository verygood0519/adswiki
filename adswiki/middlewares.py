# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent    #导入浏览器用户代理模块

class RandomUserAgentMiddlware(object):                                    #自定义浏览器代理中间件
    #随机更换Requests请求头信息的User-Agent浏览器用户代理
    def __init__(self,crawler):
        super(RandomUserAgentMiddlware, self).__init__()                   #获取上一级父类基类的，__init__方法里的对象封装值
        self.ua = UserAgent()                                               #实例化浏览器用户代理模块类
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE','random')      #获取settings.py配置文件里的RANDOM_UA_TYPE配置的浏览器类型，如果没有，默认random，随机获取各种浏览器类型

    @classmethod                                                            #函数上面用上装饰符@classmethod，函数里有一个必写形式参数cls用来接收当前类名称
    def from_crawler(cls, crawler):                                         #重载from_crawler方法
        return cls(crawler)                                                 #将crawler爬虫返回给类

    def process_request(self, request, spider):                             #重载process_request方法
        def get_ua():                                                       #自定义函数，返回浏览器代理对象里指定类型的浏览器信息
            return getattr(self.ua, self.ua_type)
        # print("ua:",get_ua())
        request.headers.setdefault('User-Agent', get_ua())                  #将浏览器代理信息添加到Requests请求

class AdswikiSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
