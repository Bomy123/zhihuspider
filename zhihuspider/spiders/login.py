# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
import time
import json
import urllib.request
import random
from zhihuspider.items import ZhihuspiderItem
from zhihuspider.config import Config
class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['zhihu.com']
    need_login = False

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
        if Config.debug:
            print(topics.__str__())
            print("ids",ids.__str__())
        url_l = []
        for idx in range(0,len(topics)):
            topic_url = "https://www.zhihu.com/topics#"+urllib.request.quote(topics[idx])
            url_l.append(topic_url)
        #yield self.create_item(type=Config.topics_type, id=ids, title=topics, url=url_l)
        return self.get_class_data(ids)


    def get_class_data(self,ids):
        self.headers["Referer"] = "https://www.zhihu.com/topics"
        # head = {
        #         "Accept": "* / *",
        #         "Accept-Encoding":"gzip, deflate, br",
        #         "Accept-Language": "zh - CN, zh;q = 0.8",
        #         "Connection": "keep - alive",
        #         "Content-Length": "90",
        #         "Content-Type": "application/x-www-form-urlencoded;charset = UTF-8",
        #         "Cookie": 'q_c1 = 65099507e9694e438e990469fe57878c|1507596840000|1492482581000;_zap = f551978a-3d50-4e97-b2b2-1588c0b13ebe;q_c1 = 65099507e9694e438e990469fe57878c | 1511421051000 | 1492482581000;d_c0 = "AAAC-tv_ugyPTo4EreeI6O2oLttWZGUyEtE=|1511487750";capsion_ticket = "2|1:0|10:1511514801|14:capsion_ticket|44:NTFhYTFlNjI0ZTRiNDQxZGFkYTRlNjllMDY3ZDBiNTc=|fe850b4c310f7cce72001796386f038ebc6ddf0349055ad5c1ccdd4918464951";aliyungf_tc = AQAAAMF1WAf7fAcA4bg8Oj1lbRVKL7oZ;_xsrf = 8b8bdf34ecd10b8fa7f172accb2cadbc;l_cap_id = "NDA2NDJhYmU1OWVlNDIwMzg0NzY5YjU0YTA2NGExNGY=|1511832896|752f769fdc840eb2414d851aefd4c7d43bac2e24";r_cap_id = "NTBiNDVhMDM2YjQxNDMwYjllM2QxM2FiMjcxYTRmODc=|1511832896|c5c635500e72d0408ceb81c5ad6c01046a842699";cap_id = "YzI5NjZjNjE5MzkyNDk4YmJkYmYyZjgyMzU3Y2NmYzM=|1511832896|cdadede9d13c4230acb853b96f5687cb3793f717";__utma = 51854390.493098.1511507142.1511768899.1511832893.11;__utmc = 51854390;__utmz = 51854390.1511832893.11.9.utmcsr = baidu | utmccn = (organic) | utmcmd = organic;__utmv = 51854390.000--|2=registration_date = 20171124 = 1 ^ 3 = entry_date = 20170418 = 1',
        #         "Host": "www.zhihu.com",
        #         "Origin": "https://www.zhihu.com",
        #         "Referer": "https://www.zhihu.com/topics",
        #         "User-Agent":random.choice(Config.user_agent_list),
        #         "X-Requested-With": "XMLHttpRequest",
        #         "X-Xsrftoken": "8b8bdf34ecd10b8fa7f172accb2cadbc"
        # }
        if Config.debug:
            print(self.headers.__str__())
        for id in ids:
            if Config.debug:
                print(id)
            url = "https://www.zhihu.com/node/TopicsPlazzaListV2"
            for i in range(0,2):
                time.sleep(4)
                self.headers["User-Agent"] = random.choice(Config.user_agent_list)
                data = {
                    "method": "next",
                    "params": '{"topic_id":'+id+', "offset":20, "hash_id":""}'
                }
                yield FormRequest(url,method="POST",headers=self.headers,formdata=data,callback=self.parse_class_page,dont_filter=True)

    def parse_class_page(self,response):
        print(response.body)

    def parse_special_page(self,response):
        pass

    def parse_question_page(self,response):
        pass

    def parse_answer_page(self,response):
        pass

    def create_item(self,type,id = None,title = None,author = None,content = None,url=None):
        item = ZhihuspiderItem()
        item["type"] = type
        item["id"] = id
        item["title"] = title
        item["author"] = author
        item["content"] = content
        item["url"] = url
        return item