import re
import time
import random
import json
from scrapy.http import Request
from zhihuspider.spiders.config import Config


class AnswerPageParser:
    def get_default_ans_page(self, rid):
        url = "https://www.zhihu.com/question/" + rid
        return [Request(url, headers=Config.headers, meta={"rid": rid}, callback=self.parse_default_ans_page)]

    def parse_default_ans_page(self,rid,response):
        data = response.xpath('//div[@id="data"]/@data-state').extract_first()
        data_o = data.replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace(
            "&nbsp;", " ")
        data_json = json.loads(data_o)
        ans_ids = self.get_ans_ids(rid,data_json)
        if Config.debug:
            print(ans_ids)
        for ans_id in ans_ids:
            print("ans_content:",self.get_ans_content(str(ans_id),data_json))
            print("ans_author:",self.get_ans_author(str(ans_id),data_json))

        print("ans_next:",self.get_ans_next(rid,data_json))


    def get_more_ans_page(self):
        pass

    def parse_more_ans_page(self):
        pass

    def get_ans_data(self):
        pass

    def parse_ans_data(self):
        pass

    def get_ans_ids(self,qid,jdata):
        question = jdata['question']
        if question:
            answer = question['answers']
            if answer:
                aids = answer[qid]
                if aids:
                    return aids['newIds']




    def get_ans_next(self,qid,jdata):
        question = jdata['question']
        if question:
            answer = question['answers']

            if answer:
                q_next = answer[qid]
                if q_next:
                    next_href = q_next['next']
                    if next_href:
                        return next_href
                    else:
                        return None

    def get_ans_content(self,id,jdata):
        entities = jdata['entities']
        if entities:
            answers = entities['answers']
            if answers:
                acontent = answers[id]
                if acontent:
                    return acontent['content']

    def get_ans_author(self,id,jdata):
        entities = jdata['entities']
        if entities:
            answers = entities['answers']
            if answers:
                acontent = answers[id]
                if acontent:
                    auinfo = acontent['author']
                    if auinfo:
                        return auinfo['name']
