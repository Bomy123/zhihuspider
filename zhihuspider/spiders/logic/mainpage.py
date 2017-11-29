import re
import time
import random
import urllib.request
from scrapy.http import Request
from scrapy.http import FormRequest

from zhihuspider.spiders.config import Config
from zhihuspider.spiders.commons import Commons

class MainPageParser(object):
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
        if self.need_login:
            pat = '"user_hash":(.*?)}'
            user_hash = re.compile(pat).findall(response.body.decode("utf-8", "ignore"))[0]
            return self.get_class_data(ids, user_hash)
        else:
            return self.get_class_default_data(ids,url_l)

    def get_class_default_data(self,ids,urls):
        time.sleep(4)
        self.headers["Referer"] = "https://www.zhihu.com/topics"
        for idx in range(0,len(urls)):
            yield [Request(urls[idx],headers=self.headers,dont_filter=True,meta={"rid":[id[idx]]},callback=self.parse_class_page)]

    def get_class_data(self,ids,user_hash):
        time.sleep(4)
        self.headers["Referer"] = "https://www.zhihu.com/topics"
        if Config.debug:
            print("get_class_data",user_hash)
        for id in ids:
            if Config.debug:
                print(id)
            url = "https://www.zhihu.com/node/TopicsPlazzaListV2"
            for i in range(0,1):
                time.sleep(4)
                self.headers["User-Agent"] = random.choice(Config.user_agent_list)
                data = {
                    "method": "next",
                    "params": '{"topic_id":'+id+', "offset":20, "hash_id":'+user_hash+'}'
                }
                if Config.debug:
                    print(data["params"])
                yield FormRequest(url,method="POST",meta = {"rid":[id]},headers=self.headers,formdata=data,callback=self.parse_class_page,dont_filter=True)

    def parse_class_page(self,response):

        #hrefs = response.xpath('//div[@class="blk"]/a[@target="_blank"]/@href').extract()
        ids = None
        accurate_urls = []
        if Config.debug:
            print("parse_class_page:",response.body.decode("utf-8","ignore"))
        if self.need_login:
            pat = 'href.*?\/(\d*?)"'
            ids = re.compile(pat).findall(response.body.decode("utf-8","ignore"))
            for id in ids:
                # tmp_l = href.splite("/")
                # id = tmp_l[len(tmp_l)-1]
                ids.append(id)
                accurate_url = "https://www.zhihu.com/topic/" + id + "/hot"
                accurate_urls.append(accurate_url)
        else:
            hrefs = response.xpath('//div[@class="blk"]/a[@target="_blank"]/@href').extract()
            titles = response.xpath('//strong/text()')
            for href in hrefs:
                tmp_l = href.splite("/")
                id = tmp_l[len(tmp_l)-1]
                ids.append(id)
                accurate_url = "https://www.zhihu.com/topic/" + id + "/hot"
                accurate_urls.append(accurate_url)

        self.create_item(type=Config.content_type,id=ids,rid=response.meta["rid"],title=titles,url=accurate_urls)

        return self.get_content_first_page(ids)
    def get_content_first_page(self,ids):
        if Config.debug:
            print("get_content_first_page:",ids)
        for id in ids:
            time.sleep(10)
            url = "https://www.zhihu.com/topic/"+id+"/hot"
            if Config.debug:
                print(url)
            yield [Request(url=url,headers=self.headers,meta={"rid":id},callback=self.parse_content_first_page)]

    def parse_content_first_page(self,response):
        if Config.debug:
            print("parse_content_first_page")
        print(response.xpath('//div[@class="feed-item feed-item-hook  folding"]/@data-score'))

    def get_content_page(self,ids):
        for id in ids:
            url = "https://www.zhihu.com/topic"+id+"/hot"
            pass

    def parse_content_page(self,ids):
        for id in ids:
            url = "https://www.zhihu.com/topic"+id+"/hot"
            pass
    def parse_special_first_page(self,response):
        pass

    def parse_question_page(self,response):
        pass

    def parse_answer_page(self,response):
        pass

