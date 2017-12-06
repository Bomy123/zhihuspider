import re
import time
import json
from lxml import html
from scrapy.http import Request
from scrapy.http import FormRequest
from zhihuspider.spiders.config import Config
from zhihuspider.spiders.commons import Commons
from zhihuspider.spiders.logic.professionpage import ProfesionPageParser
from zhihuspider.spiders.logic.questionpage import QuestionPageParser


class ArticlePageParser:
    proparser = None
    quesparser = None

    def __init__(self):
        self.proparser = ProfesionPageParser()
        self.quesparser = QuestionPageParser()

    def get_article_default_page(self, ids):
        return 0
        if Config.debug:
            print("get_content_first_page:", ids)
        for id in ids:
            time.sleep(2)
            url = "https://www.zhihu.com/topic/" + id + "/hot"
            if Config.debug:
                print(url)
            yield Request(url=url, headers=Config.headers, meta={"rid": id}, callback=self.parse_article_default_page)

    def parse_article_default_page(self, response):
        if Config.debug:
            print("parse_content_first_page")
        hrefs = response.xpath('//h2/a[@data-za-element-name="Title"]/@href').extract()
        titles = response.xpath('//h2/a[@data-za-element-name="Title"]/text()').extract()
        scores = response.xpath('//div[@class="feed-item feed-item-hook  folding"]/@data-score').extract()
        rid = response.meta["rid"]
        if Config.login:
            self.get_more_article_data(response.meta["rid"], scores[len(scores) - 1])
        for idx in range(0, len(hrefs)):
            accurate_url = "https://www.zhihu.com" + hrefs[idx]
            if Config.debug:
                print("parse_content_first_page", accurate_url)
            temp_str = hrefs[idx].split("/")
            id = temp_str[2]
            if Config.debug:
                print("parse_article_default_page", temp_str[1])
            if temp_str[1] == "q":
                if Config.debug:
                    print("parse_article_default_page", "专栏")
                Commons.commit_item(datatype=Config.artical_type, id=[id], rid=[rid], title=[titles[idx]], author=None,
                                    content=None, url=[accurate_url], content_type=["专栏"])
                return self.proparser.get_default_pro_data(id, response.meta["rid"], accurate_url)
            else:
                if Config.debug:
                    print("parse_article_default_page", "问答")
                Commons.commit_item(datatype=Config.artical_type, id=[id], rid=[rid], title=[titles[idx]], author=None,
                                    content=None, url=[accurate_url], content_type=["问答"]
                                    )
                print(accurate_url)
                return self.quesparser.get_default_ques_page(id, accurate_url)

    def get_more_article_data(self, id, data_score):
        return self.get_article_data(id, data_score)

    def get_article_data(self, id, data_score):
        url = "https://www.zhihu.com/topic/" + id + "/hot"
        data = {
            "start": 0,
            "offset": data_score
        }
        return [
            FormRequest(url, formdata=data, meta={"rid": id}, headers=Config.headers, callback=self.parse_article_data)]

    def parse_article_data(self, response):
        data_o = response.body.decode("utf-8", "ignore")
        data_json = json.loads(data_o)
        rid = response.meta["rid"]
        msg = data_json["msg"]
        scores = None
        if msg:
            content = msg[1]
            hdata = html.document_fromstring(content)
            titles = hdata.xpath('//a[@data-za-element-name="Title"]/text()')
            hrefs = response.xpath('//h2/a[@data-za-element-name="Title"]/@href').extract()
            for idx in range(0, len(hrefs)):
                accurate_url = "https://www.zhihu.com" + hrefs[idx]
                if Config.debug:
                    print("parse_content_first_page", accurate_url)
                temp_str = hrefs[idx].split("/")
                id = temp_str[2]
                if Config.debug:
                    print("parse_article_default_page", temp_str[1])
                if temp_str[1] == "q":
                    if Config.debug:
                        print("parse_article_default_page", "专栏")
                    Commons.commit_item(datatype=Config.artical_type, id=[id], rid=[rid], title=[titles[idx]],
                                        author=None,
                                        content=None, url=[accurate_url], content_type=["专栏"])
                    return self.proparser.get_default_pro_data(id, response.meta["rid"], accurate_url)
                else:
                    if Config.debug:
                        print("parse_article_default_page", "问答")
                    Commons.commit_item(datatype=Config.artical_type, id=[id], rid=[rid], title=[titles[idx]],
                                        author=None,
                                        content=None, url=[accurate_url], content_type=["问答"]
                                        )
                    print(accurate_url)
                    return self.quesparser.get_default_ques_page(id, accurate_url)
            scores = hdata.xpath('//div[@class="feed-item feed-item-hook  folding"]/@data-score').extrace()
        yield self.get_article_data(rid, scores[len(scores) - 1])
