import re
from scrapy.http import FormRequest
import urllib.request
import random
from zhihuspider.spiders.config import Config
from zhihuspider.spiders.commons import Commons
from zhihuspider.spiders.logic.classpage import ClassPageParser

class MainPageParser(object):
    classparser = None
    def __init__(self):
        self.classparser = ClassPageParser()
    def parse_main_page(self,response):
        topics = response.xpath("//li[@class='zm-topic-cat-item']/a/text()").extract()
        ids = response.xpath("//li[@class='zm-topic-cat-item']/@data-id").extract()

        if Config.debug:
            print(topics.__str__())
            print("ids",ids.__str__())
        url_l = []
        user_hash = ""
        if Config.login:
            pat = '"user_hash":(.*?)}'
            user_hash = re.compile(pat).findall(response.body.decode("utf-8", "ignore"))[0]
        for idx in range(0,len(topics)):
            topic_url = "https://www.zhihu.com/topics#"+urllib.request.quote(topics[idx])
            url_l.append(topic_url)
            id = ids[idx]
            Commons.commit_item(datatype=Config.topics_type, id=[id], title=[topics[idx]], url=[topic_url])
            self.count = 0
            Config.headers["Referer"] = "https://www.zhihu.com/topics"
            if Config.debug:
                print("get_class_data", user_hash)
            if Config.debug:
                print(id)
            url = "https://www.zhihu.com/node/TopicsPlazzaListV2"
            Config.headers["User-Agent"] = random.choice(Config.user_agent_list)
            for i in range(0, 10):
                data = {
                    "method": "next",
                    "params": '{"topic_id":' + id + ', "offset":' + str(i * 20) + ',"hash_id":"' + user_hash + '"}'
                }
                if Config.debug:
                    print(data["params"])
                yield FormRequest(url, method="POST", meta={"rid": id, "hash": user_hash}, headers=Config.headers,
                                  formdata=data,
                                  callback=self.classparser.parse_class_page, dont_filter=True)
