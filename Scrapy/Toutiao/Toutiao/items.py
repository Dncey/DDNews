# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ToutiaoItem(scrapy.Item):

    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    digest = scrapy.Field()
    time = scrapy.Field()
    digest_label = scrapy.Field()
    category = scrapy.Field()
    content = scrapy.Field()
    index_url = scrapy.Field()
    index_urls = scrapy.Field()
    # 浏览数量
    impression_count = scrapy.Field()
    #评论数量
    comment_count = scrapy.Field()
    #作者id
    creator_uid = scrapy.Field()
    #作者头像
    source_avatar_url = scrapy.Field()

class TitleSpiderItem(scrapy.Item):
    title = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()


