import re
import time
import random
import json
from scrapy.http import Request
from zhihuspider.spiders.config import Config


def AnswerPageParser():
    def get_default_ans_page(self, rid):
        url = "https://www.zhihu.com/question/" + rid
        return [Request(url, headers=Config.headers, meta={"rid": id}, callback=self.parse_default_ans_page)]

    def parse_default_ans_page(self, response):
        data = response.xpath('//div[@id="data"]/@data-state').extract_first()
        data_o = data.replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace(
            "&nbsp;", " ")
        data_json = json.loads(data_o)
        print(data_json)

    def get_more_ans_page(self):
        pass

    def parse_more_ans_page(self):
        pass

    def get_ans_data(self):
        pass

    def parse_ans_data(self):
        pass
