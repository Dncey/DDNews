# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import re
from scrapy.pipelines.images import ImagesPipeline
from scrapy_redis.pipelines import RedisPipeline
import requests
from fdfs_client.client import Fdfs_client

class ToutiaoPipeline(object):
    def open_spider(self, spider):  # 在爬虫开启的时候仅执行一次
        # if spider.name == 'toutiao':
        self.f = open('/home/python/Desktop/Scrapy/Toutiaojson2.txt', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        # if spider.name == 'toutiao':
        item = dict(item)
            # client = Fdfs_client('fastdfs/client.conf')
            # flag= True
            # for image_url in item['image_urls']:
            #     image_data = requests.get(image_url,headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Mobile Safari/537.36'}).content
            #     if not image_data:
            #          continue
            #     ret = client.upload_by_buffer(image_data)
            #     new_url = 'http://image.meiduo.site:8888/'+ret['Remote file_id']
            #     item['content'] = item['content'].replace(image_url,new_url)
            #     if flag:
            #         item['index_url']=new_url
            #         flag=False
        print('*'*100)
        self.f.write(json.dumps(item, ensure_ascii=False) + '\n')
        return item

    def close_spider(self, spider):  # 在爬虫关闭的时候仅执行一次
        # if spider.name == 'toutiao':
        self.f.close()


