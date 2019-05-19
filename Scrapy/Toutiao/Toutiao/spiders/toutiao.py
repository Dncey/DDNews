#encoding=utf-8
import scrapy
from scrapy.http import Request
from scrapy_redis.utils import bytes_to_str
from Toutiao.items import ToutiaoItem

import json
import time
import execjs
import re
import random
from scrapy_redis.spiders import RedisSpider
from redis import StrictRedis


# class TouTiaoSpider(scrapy.Spider):
class TouTiaoSpider(RedisSpider):

    #重写起始从redis中获取的url
    # def make_request_from_data(self, data):
    #     Honey = json.loads(self.get_js())
    #     eas = Honey['as']
    #     ecp = Honey['cp']
    #     signature = Honey['_signature']
    #
    #     url = bytes_to_str(data, self.redis_encoding)
    #
    #     url = url.format(random.choice(channel_list),'0','0',eas,ecp,signature)
    #     yield self.make_requests_from_url(url)
    #
    # def make_requests_from_url(self, url):
    #     """ This method is deprecated. """
    #     cookies_str = 'tt_webid=6676409537924630030; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6676409537924630030; uuid="w:4f4872f5165c4c89a174480375e52901"; __tasessionId=dyku7ui3e1554810361366'
    #     cookies_dict = {i.split('=')[0]: i.split('=')[1] for i in cookies_str.split('; ')}
    #     return Request(url, cookies = cookies_dict,dont_filter=True)
    #
    # def make_requests_from_url_DontRedirect(self, url):
    #     """ This method is deprecated. """
    #
    #     # 注解: 在这一步进行改写，将原始的originalUrl放到meta信息中进行传递。
    #     #      如果想指定不允许重定向，也是在meta信息中，加入：meta={'dont_redirect':True}
    #     #      不过，在这里，推荐的做法，还是允许跳转，但是记录原始链接originalUrl
    #     return Request(url, meta={'originalUrl': url}, dont_filter=True)

    name = 'toutiao'
    # ----3 注销start_urls&allowed_domains
    # # 修改允许的域
    # allowed_domains = ['toutiao.com']
    # # 修改起始的url

    # start_urls = ['https://www.toutiao.com/api/pc/feed/?category={}&utm_source=toutiao&widen=1&max_behot_time={}&max_behot_time_tmp={}&tadrequire=true&as={}&cp={}&_signature={}']

    # ----4 设置redis-key
    redis_key = 'Dncey'

    # ----5 设置__init__
    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        super(TouTiaoSpider, self).__init__(*args, **kwargs)

    #开启分布式爬虫这个函数不会执行
    # def start_requests(self):
    #     cookies_str = 'tt_webid=6676409537924630030; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6676409537924630030; uuid="w:4f4872f5165c4c89a174480375e52901"; __tasessionId=dyku7ui3e1554810361366'
    #     cookies_dict = {i.split('=')[0]:i.split('=')[1]for i in cookies_str.split('; ')}
    #     for i in range(0,30):
    #         Honey = json.loads(self.get_js())
    #         eas =Honey['as']
    #         ecp = Honey['cp']
    #         signature = Honey['_signature']
    #
    #         yield scrapy.Request(self.start_urls[0].format(random.choice(channel_list),'0','0',eas,ecp,signature),cookies = cookies_dict,dont_filter=True)


    def get_js(self):
        f = open(r"/home/python/Desktop/Scrapy/Toutiao/Toutiao/judge/signature.js", 'r',
                 encoding='UTF-8')  ##打开JS文件
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
        ctx = execjs.compile(htmlstr)
        return ctx.call('get_as_cp_signature')

    def parse(self,response):

        print(response.request.headers)
        # theCategoryUrl = response.url  # 品类的链接
        # isRedirect = False  # 记录是否发生了跳转，默认是记为 无重定向
        # redirectUrl = ""  # 记录跳转后的页面，默认为空
        # if "originalUrl" in response.meta:
        #     if response.meta["originalUrl"] == response.url:  # 说明没有发生页面跳转
        #         isRedirect = False
        #     else:
        #         # 发生了跳转，打上标记， 并更新categoryUrl为original，方便找到categoryInfo的信息，并记录跳转后的页面
        #         isRedirect = True
        #         theCategoryUrl = response.meta["originalUrl"]
        #         redirectUrl = response.url
        # else:
        #     # 如果后期没有这个机制的话，那就恢复原来的处理机制，啥也不做
        #     pass
        # 娱乐、游戏、体育、财经、热文、科技、军事、国际
        channel_list = ['news_entertainment', 'news_game', 'news_sports', 'news_finance', 'news_hot', 'news_tech','news_military', 'funny', 'news_world']

        url = 'https://www.toutiao.com/api/pc/feed/?category={}&utm_source=toutiao&widen=1&max_behot_time={}&max_behot_time_tmp={}&tadrequire=true&as={}&cp={}&_signature={}'

        while True:

            Honey = json.loads(self.get_js())
            eas = Honey['as']
            ecp = Honey['cp']
            signature = Honey['_signature']

            yield scrapy.Request(url.format(random.choice(channel_list),'0','0',eas,ecp,signature),callback=self.process_category,dont_filter=True)


    def process_category(self,response):
        try:
            sites = json.loads(response.body_as_unicode())['data']
        except Exception as e:
            return

        for site in sites:
            info_dict = {}
            info_dict['title'] = site.get('title')
            info_dict['author'] = site.get('source')
            info_dict['digest_label'] = site.get('label')
            info_dict['digest'] = site.get('abstract')
            info_dict['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(site.get('behot_time')))
            info_dict['category'] = site.get('chinese_tag')
            info_dict['index_url'] = site.get('image_url')
            info_dict['index_urls'] = site.get('index_urls')
            #作者头像
            info_dict['source_avatar_url'] = site.get('media_avatar_url')
            #下面拼接文章url
            id = site['group_id']
            regx = re.compile('.*category=(.*?)&')
            refer_url = regx.findall(response.request.url)
            refer_url = refer_url[0]
            # 设置链接来往位置
            referer = 'https://www.toutiao.com/ch/%s/' % refer_url

            headers  = {
                'referer':referer
            }

            url =  'https://m.toutiao.com/i{}/info/?i={}'.format(id,id)
            yield scrapy.Request(url,callback=self.detail_parse,meta=info_dict,dont_filter=False,headers=headers)



    def detail_parse(self,response):
        info_dict = response.meta
        item = ToutiaoItem()
        site = json.loads(response.body_as_unicode())['data']
        item['title'] = info_dict['title']
        item['author'] = info_dict['author']
        item['digest'] = info_dict['digest'] #文章简要
        item['time'] = info_dict['time'] #时间
        item['digest_label']=info_dict['digest_label']#文章关键字
        item['category'] = info_dict['category']#文章分类
        item['index_url'] = info_dict['index_url']#文章索引图片
        item['index_urls'] = info_dict['index_urls']#文章所有图片列表，没有为空
        #浏览数量
        item['impression_count'] = site['impression_count']
        #评论数量
        item['comment_count'] = site['comment_count']
        #作者id
        item['creator_uid'] = site['creator_uid']

        #作者头像url
        item['source_avatar_url'] = info_dict['source_avatar_url']

        content = site['content']
        #匹配出文章中的url
        # reg = re.compile('.*?img src="(https.*?)"')
        #文章的图片所有url
        # image_urls = reg.findall(content)

        item['content'] =content


        yield item



#