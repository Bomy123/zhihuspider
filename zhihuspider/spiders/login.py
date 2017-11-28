# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
import time
import json
import urllib.request
import random
from zhihuspider.items import ZhihuspiderItem
from zhihuspider.config import Config
from zhihuspider.pipelines import ZhihuspiderPipeline
import re
class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['zhihu.com']
    need_login = True
    pipeline = None
    headers = {
        "Host": "www.zhihu.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Upgrade - Insecure - Requests": "1",
        "Connection": "keep-alive",
        "Origin": "https://www.zhihu.com",
        "Referer": "https://www.zhihu.com/topics",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
        #"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    def start_requests(self):
        self.pipeline = ZhihuspiderPipeline()
        self.headers["User-Agent"] = random.choice(Config.user_agent_list)
        if self.need_login:
            url = "https://www.zhihu.com/captcha.gif?r=" + str(int(time.time() * 1000)) + "&type=login&lang=en"
            print(url)
            return [Request(url=url,
                            headers=self.headers, callback=self.parse)]
        else:
            return [Request("https://www.zhihu.com/topics",headers=self.headers,callback=self.parse_main_page)]


    def parse(self, response):
        with open("./1.gif","wb") as img:
            img.write(response.body)
        url = "https://www.zhihu.com/"
        return [Request(url, headers=self.headers, callback=self.do_login, errback=self.erro)]

    def do_login(self,response):

        capt_str = input("请输入验证码：")
        print(capt_str)
        xsrf = response.xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print("*********************************************************************88xsrf", xsrf)
        url = "https://www.zhihu.com/login/phone_num"
        self.headers["X-Xsrftoken"] = xsrf
        print(self.headers.__str__())
        data = {
            "password": "420321@zmb",
            "captcha": capt_str,
            "phone_num": "15976898663",
            "_xsrf": xsrf,
            "captcha_type": "en",
        }
        return [
            FormRequest(url, method="POST", formdata=data,headers=self.headers, callback=self.is_login_success,errback=self.erro)]

    def erro(self, e):
        print(e.__str__())

    def is_login_success(self, response):
        print(response.body)
        res = json.loads(response.body.decode("utf-8","ignore"))
        if res["r"] == 0:
            print("登陆成功")
            return [Request("https://www.zhihu.com/topics", headers=self.headers, callback=self.parse_main_page)]
        else:
            print("登陆失败")

    def parse_main_page(self,response):
        topics = response.xpath("//li[@class='zm-topic-cat-item']/a/text()").extract()
        ids= response.xpath("//li[@class='zm-topic-cat-item']/@data-id").extract()
        pat = '"user_hash":(.*?)}'
        user_hash = re.compile(pat).findall(response.body.decode("utf-8","ignore"))[0]
        if Config.debug:
            print(topics.__str__())
            print("ids",ids.__str__())
        url_l = []
        for idx in range(0,len(topics)):
            topic_url = "https://www.zhihu.com/topics#"+urllib.request.quote(topics[idx])
            url_l.append(topic_url)
        self.create_item(type=Config.topics_type, id=ids, title=topics, url=url_l)
        if self.need_login:
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
        if self.need_login:
            pat = 'href.*?\/(\d*?)"'
            ids = re.compile(pat).findall(response.body.decode("utf-8","ignore"))
        else:
            ids = response.xpath('//a[@data-za-element-name="Title"]/@data-id').extract()
        if Config.debug:
            print("parse_class_page:",ids.__str__(),response.body.decode("utf-8","ignore"))

        titles = response.xpath('//image/@alt')
        accurate_urls  = []
        for id in ids:
            # tmp_l = href.splite("/")
            # id = tmp_l[len(tmp_l)-1]
            ids.append(id)
            accurate_url = "https://www.zhihu.com/topic/"+id+"/hot"
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

    def create_item(self,type,id = None,rid = None,title = None,author = None,content = None,url=None):
        item = ZhihuspiderItem()
        item["type"] = type
        item["id"] = id
        item["rid"] = rid
        item["title"] = title
        item["author"] = author
        item["content"] = content
        item["url"] = url
        self.pipeline.process_item(item = item,spider=self)