import re
import urllib.request

from zhihuspider.spiders.config import Config
from zhihuspider.spiders.commons import Commons
from zhihuspider.spiders.logic.classpage import ClassPageParser


class MainPageParser(object):
    classparser = None
    def __init__(self):
        self.classparser = ClassPageParser()
    def parse_main_page(self,response):
        if Config.debug:
            print(response.body)
        topics = response.xpath("//li[@class='zm-topic-cat-item']/a/text()").extract()
        ids = response.xpath("//li[@class='zm-topic-cat-item']/@data-id").extract()

        if Config.debug:
            print(topics.__str__())
            print("ids",ids.__str__())
        url_l = []
        for idx in range(0,len(topics)):
            topic_url = "https://www.zhihu.com/topics#"+urllib.request.quote(topics[idx])
            url_l.append(topic_url)
        Commons.commit_item(datatype=Config.topics_type, id=ids, title=topics, url=url_l)
        if Config.login:
            pat = '"user_hash":(.*?)}'
            user_hash = re.compile(pat).findall(response.body.decode("utf-8", "ignore"))[0]
            return self.classparser.get_class_data(ids, user_hash)
        else:
            return self.classparser.get_class_default_data(ids,url_l)



