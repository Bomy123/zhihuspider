
import random
import json
from lxml import html
from scrapy.http import FormRequest,Request

from zhihuspider.spiders.config import Config
from zhihuspider.spiders.commons import Commons
from zhihuspider.spiders.logic.articalpage import ArticlePageParser


class ClassPageParser:
    articleparser = None
    count  = 0

    def __init__(self):
        self.articalparser = ArticlePageParser()

    def get_class_default_data(self, id, user_hash=""):
        Config.headers["Referer"] = "https://www.zhihu.com/topics"
        print(id)
        # for idx in range(0, len(urls)):
        #     time.sleep(2)
        #     if Config.debug:
        #         print("get_class_default_data:",ids[idx])
        #     yield Request(urls[idx], headers=Config.headers, dont_filter=True,
        #                    meta={"rid": [ids[idx]], "user_hash": user_hash},
        #                    callback=self.parse_class_default_data)
        return self.get_class_data(id,user_hash)

    def parse_class_default_data(self, response):
        hrefs = response.xpath('//div[@class="blk"]/a[@target="_blank"]/@href').extract()
        titles = response.xpath('//strong/text()').extract()
        print("parser_class_default_data:", titles)
        ids = []
        accurate_urls = []
        for href in hrefs:
            tmp_l = href.split("/")
            id = tmp_l[len(tmp_l) - 1]
            ids.append(id)
            accurate_url = "https://www.zhihu.com/topic/" + id + "/hot"
            accurate_urls.append(accurate_url)
            if Config.login:
                user_hash = response.meta["user_hash"]
                self.get_more_class_data(id, user_hash)
        Commons.commit_item(datatype=Config.class_type, id=ids, rid=response.meta["rid"], title=titles, url=accurate_urls)
        return self.articalparser.get_article_default_page(ids)

    def get_more_class_data(self, id, user_hash):
        return self.get_class_data(id, user_hash)

    def get_class_data(self, id, user_hash):
        self.count = 0
        Config.headers["Referer"] = "https://www.zhihu.com/topics"
        if Config.debug:
            print("get_class_data", user_hash)
        if Config.debug:
            print(id)
        url = "https://www.zhihu.com/node/TopicsPlazzaListV2"
        Config.headers["User-Agent"] = random.choice(Config.user_agent_list)
        for i in range(0,10):
            data = {
                "method": "next",
                "params": '{"topic_id":' + id + ', "offset":'+str(i*20)+',"hash_id":"' + user_hash + '"}'
            }
            if Config.debug:
                print(data["params"])
            yield FormRequest(url, method="POST", meta={"rid": id,"hash":user_hash}, headers=Config.headers, formdata=data,
                              callback=self.parse_class_page, dont_filter=True)

    def parse_class_page(self, response):
        data_o = response.body.decode("utf-8", "ignore")
        #print("data_o",data_o)

        data_json = json.loads(data_o)
        rid = response.meta["rid"]
        msg = data_json["msg"]
        print(msg[0])
        if len(msg) >0:
            ids = []
            accurate_urls = []
            titles = []
            for imsg in msg:
                hdata = html.document_fromstring(imsg)
                href = hdata.xpath('//div[@class="blk"]/a[@target="_blank"]/@href')[0]
                title =hdata.xpath('//strong/text()')[0]
                # if Config.debug:
                #     print("parse_class_page:", response.body.decode("utf-8", "ignore"))
                #pat = 'href.*?\/(\d*?)"'
                #ids = re.compile(pat).findall(response.body.decode("utf-8", "ignore"))
                tmp_l = href.split("/")
                id = tmp_l[len(tmp_l)-1]
                ids.append(id)
                accurate_url = "https://www.zhihu.com/"+href
                accurate_urls.append(accurate_url)
                titles.append(title)
                if Config.debug:
                    print("accurate_urls",accurate_urls,ids)
            if Config.debug:
                print(accurate_urls)
            Commons.commit_item(datatype=Config.class_type, id=ids, rid=[rid], title=titles, url=accurate_urls)
            if Config.debug:
                print("get_content_first_page:", ids)
            for id in ids:
                url = "https://www.zhihu.com/topic/" + id + "/hot"
                if Config.debug:
                    print(url)
                yield Request(url=url, headers=Config.headers, meta={"rid": id},
                              callback=self.articalparser.parse_article_default_page)



