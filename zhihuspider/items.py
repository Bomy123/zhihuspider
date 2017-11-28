# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type = scrapy.Field()
    id = scrapy.Field()
    rid = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
