
import json
from scrapy.http import Request
from zhihuspider.spiders.config import Config
from zhihuspider.spiders.commons import Commons

class AnswerPageParser:
    def get_default_ans_page(self, rid):
        url = "https://www.zhihu.com/question/" + rid
        return [Request(url, headers=Config.headers, meta={"rid": rid}, callback=self.parse_default_ans_page)]

    def parse_default_ans_page(self,response):
        rid = response.meta["id"]
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
            Commons.commit_item(content=self.get_ans_content(str(ans_id),data_json),author=self.get_ans_author(str(ans_id),data_json),id=ans_id,rid=rid)
        if self.get_ans_author(rid,data_json) > len(ans_ids):
            nextpage = self.get_ans_next(rid, data_json)
            return self.get_more_ans_page(rid,nextpage)


    def get_more_ans_page(self,qid,url):
        yield [Request(url = url,headers=Config.headers,meta={"rid",qid},callback=self.parse_more_ans_page)]

    def parse_more_ans_page(self,response):
        rid = response.meta["rid"]
        data_o = response.body.decode("utf-8","ignore")
        data_json = json.loads(data_o)
        resdata = self.get_more_ans_page(response.meta["rid"],data_json)
        for idata in resdata:
            Commons.commit_item(id=[idata["id"]],content=[idata["content"]],author=[idata["author"]],rid=rid)
        if self.get_isend(data_json):
            return self.get_more_ans_page(rid,self.get_more_next(data_json))



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

    def get_ans_author(self,qid,jdata):
        entities = jdata['entities']
        if entities:
            questions = entities['questions']
            if questions:
                qcontent = questions[qid]
                if qcontent:
                    return qcontent["answerCount"]

    def get_isend(self,jdata):
        paging = jdata["paging"]
        if paging:
            return paging["is_end"]

    def get_more_ans_data(self,qid,jdata):
        data = jdata["data"]
        res = []
        if data:
            for idata in data:
                content = idata["content"]
                if content:
                    res.append({"content":content})
                aid = idata["id"]
                if aid:
                    res.append({"id"},aid)
                author = content["author"]
                if author:
                    name  = author["name"]
                    if name:
                        res.append({"name":name})
        return res

    def get_more_next(self,jdata):
        paging = jdata["paging"]
        if paging:
            return paging["next"]