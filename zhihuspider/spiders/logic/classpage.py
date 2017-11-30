import re
import time
import random
from scrapy.http import Request
from scrapy.http import FormRequest

from zhihuspider.spiders.config import Config
from zhihuspider.spiders.commons import Commons
from zhihuspider.spiders.logic.articalpage import ArticlePageParser


class ClassPageParser:

    articleparser = None

    def __init__(self):
        self.articalparser = ArticlePageParser()

    def get_class_default_data(self, ids,rid, urls,user_hash = None):
        time.sleep(4)
        Config.headers["Referer"] = "https://www.zhihu.com/topics"
        for idx in range(0, len(urls)):
            yield [Request(urls[idx], headers=Config.headers, dont_filter=True, meta={"rid": [id[idx]],"user_hash":user_hash},
                           callback=self.parse_class_page)]

    def parse_class_default_data(self,response):
        hrefs = response.xpath('//div[@class="blk"]/a[@target="_blank"]/@href').extract()
		titles = response.xpath('//strong/text()')
		ids = []
		accurate_urls = []
		for href in hrefs:
			tmp_l = href.splite("/")
			id = tmp_l[len(tmp_l) - 1]
			ids.append(id)
			accurate_url = "https://www.zhihu.com/topic/" + id + "/hot"
			accurate_urls.append(accurate_url)
			if Config.login:
				user_hash = response.meta["user_hash"]
				self.get_more_class_data(id,user_hash)
				get_more_class_data(id,user_hash)
		Commons.commit_item(type=Config.class_type, id=[id], rid=response.meta["rid"], title=titles, url=accurate_urls)
		return self.articalparser.get_content_default_page(ids)

	def get_more_class_data(self,id,user_hash):
		return get_class_data(id,user_hash)
    def get_class_data(self, id, user_hash):
        time.sleep(4)
        self.headers["Referer"] = "https://www.zhihu.com/topics"
        if Config.debug:
            print("get_class_data", user_hash)
        if Config.debug:
            print(id)
        url = "https://www.zhihu.com/node/TopicsPlazzaListV2"
        for i in range(0, 1):
            time.sleep(4)
            self.headers["User-Agent"] = random.choice(Config.user_agent_list)
            data = {
                "method": "next",
                "params": '{"topic_id":' + id + ', "offset":20, "hash_id":' + user_hash + '}'
            }
            if Config.debug:
                print(data["params"])
            yield FormRequest(url, method="POST", meta={"rid": [id]}, headers=self.headers, formdata=data,
                                  callback=self.parse_class_page, dont_filter=True)

    def parse_class_page(self, response):
        # hrefs = response.xpath('//div[@class="blk"]/a[@target="_blank"]/@href').extract()
        ids = None
        accurate_urls = []
        if Config.debug:
            print("parse_class_page:", response.body.decode("utf-8", "ignore"))
        pat = 'href.*?\/(\d*?)"'
        ids = re.compile(pat).findall(response.body.decode("utf-8", "ignore"))
        for id in ids:
                # tmp_l = href.splite("/")
                # id = tmp_l[len(tmp_l)-1]
            ids.append(id)
            accurate_url = "https://www.zhihu.com/topic/" + id + "/hot"
            accurate_urls.append(accurate_url)

        Commons.commit_item(type=Config.content_type, id=ids, rid=response.meta["rid"], title=titles, url=accurate_urls)
        return self.articalparser.get_content_first_page(ids)
