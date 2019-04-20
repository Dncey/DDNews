# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#中间件随机请求头
import random
from scrapy import signals
from Toutiao.settings import USER_AGENTS_LIST,PROXY_LIST
import re
import base64

class UserAgentMiddleware(object):

    #设置随机代理,# 设置refer
    def process_request(self,request,spider):
        UserAgent = random.choice(USER_AGENTS_LIST)
        request.headers['User-Agent'] = UserAgent
        # 匹配出url分类字符
        regx = re.compile('.*category=(.*?)&')
        refer_url = regx.findall(request.url)
        if refer_url:
            refer_url = refer_url[0]
            # 设置链接来往位置
            referer = 'https://www.toutiao.com/ch/%s/' % refer_url

            request.headers['referer'] = referer



class RandomProxy(object):

    def process_request(self, request, spider):
        proxy = random.choice(PROXY_LIST)
        print(proxy)
        if 'user_passwd' in proxy:
            # 对账号密码进行编码，python3中base64编码的数据必须是bytes类型，所以需要encode
            b64_up = base64.b64encode(proxy['user_passwd'].encode())
            # 设置认证
            request.headers['Proxy-Authorization'] = 'Basic ' + b64_up.decode()
            # 设置代理
            request.meta['proxy'] = proxy['ip_port']
        else:
            # 设置代理
            request.meta['proxy'] = proxy['ip_port']


