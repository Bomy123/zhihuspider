import re
import time
import random
from scrapy.http import Request
from scrapy.http import FormRequest
from zhihuspider.spiders.config import Config
from zhihuspider.spiders.commons import Commons


class ArticlePageParser:
    def get_content_first_page(self, ids):
        if Config.debug:
            print("get_content_first_page:", ids)
        for id in ids:
            time.sleep(10)
            url = "https://www.zhihu.com/topic/" + id + "/hot"
            if Config.debug:
                print(url)
            yield [Request(url=url, headers=self.headers, meta={"rid": id}, callback=self.parse_content_first_page)]

    def parse_content_first_page(self, response):
        if Config.debug:
            print("parse_content_first_page")
        print(response.xpath('//div[@class="feed-item feed-item-hook  folding"]/@data-score'))

    def get_content_page(self, ids):
        for id in ids:
            url = "https://www.zhihu.com/topic" + id + "/hot"
            pass

    def parse_content_page(self, ids):
        for id in ids:
            url = "https://www.zhihu.com/topic" + id + "/hot"
            pass

    def parse_special_first_page(self, response):
        pass

    def parse_question_page(self, response):
        pass

    def parse_answer_page(self, response):
        pass