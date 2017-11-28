# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
import time
import json
import urllib.request
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
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    def start_requests(self):
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
        for topic in topics:
            yield  self.parse_artical_page(topic)
        print(topics.__str__())

    def get_artical_page(self,topic):
        url = "https://www.zhihu.com/topics#"+urllib.request.quote(topic)
        return [Request(url,headers=self.headers,callback=self.parse_artical_page)]

    def parse_artical_page(self,response):
        pass

    def parse_special_page(self,response):
        pass

    def parse_question_page(self,response):
        pass

    def parse_answer_page(self,response):
        pass