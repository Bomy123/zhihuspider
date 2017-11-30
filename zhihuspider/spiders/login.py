# -*- coding: utf-8 -*-
import json
import random
import re
import time
import urllib.request

import scrapy
from scrapy.http import Request, FormRequest

from zhihuspider.items import ZhihuspiderItem
from zhihuspider.pipelines import ZhihuspiderPipeline
from zhihuspider.spiders.config import Config
from zhihuspider.spiders.logic.mainpage import MainPageParser

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['zhihu.com']
    mainparser = None


    def start_requests(self):
        self.mainparser = MainPageParser()
        Config.headers["User-Agent"] = random.choice(Config.user_agent_list)
        if Config.login:
            url = "https://www.zhihu.com/captcha.gif?r=" + str(int(time.time() * 1000)) + "&type=login&lang=en"
            print(url)
            return [Request(url=url,
                            headers=Config.headers, callback=self.parse)]
        else:
            return [Request("https://www.zhihu.com/topics",headers=Config.headers,callback=self.mainparser.parse_main_page)]


    def parse(self, response):
        with open("./1.gif","wb") as img:
            img.write(response.body)
        url = "https://www.zhihu.com/"
        return [Request(url, headers=Config.headers, callback=self.do_login, errback=self.erro)]

    def do_login(self,response):

        capt_str = input("请输入验证码：")
        print(capt_str)
        xsrf = response.xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print("*********************************************************************88xsrf", xsrf)
        url = "https://www.zhihu.com/login/phone_num"
        Config.headers["X-Xsrftoken"] = xsrf
        print(Config.headers.__str__())
        data = {
            "password": "420321@zmb",
            "captcha": capt_str,
            "phone_num": "15976898663",
            "_xsrf": xsrf,
            "captcha_type": "en",
        }
        return [
            FormRequest(url, method="POST", formdata=data,headers=Config.headers, callback=self.is_login_success,errback=self.erro)]

    def erro(self, e):
        print(e.__str__())

    def is_login_success(self, response):
        print(response.body)
        res = json.loads(response.body.decode("utf-8","ignore"))
        if res["r"] == 0:
            print("登陆成功")
            return [Request("https://www.zhihu.com/topics", headers=Config.headers, callback=self.mainparser.parse_main_page)]
        else:
            print("登陆失败")
