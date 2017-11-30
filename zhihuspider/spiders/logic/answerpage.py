import re
import time
import random
import json
from scrapy.http import Request
from scrapy.http import FormRequest
from zhihuspider.spiders.config import Config
from zhihuspider.spiders.commons import Commons
from zhihuspider.spiders.logic.professionpage import ProfesionPageParser
from zhihuspider.spiders.logic.questionpage import QuestionPageParser
def AnswerPageParser:
	def get_default_ans_page(self,rid):
		url = "https://www.zhihu.com/question/"+rid
		return [Request(url,headers = Config.headers,meta = {"rid":id},callback = self.parse_default_ans_page)]
	def parse_default_ans_page(self,response):
		data = response.xpath('//div[@id="data"]/@data-state')
		pat = '&quot;content&quot;(.*?)&quot;commentCount&quot'
		contents = re.compile(pat).findall(data)

	def get_more_ans_page(self):
		pass

	def parse_more_ans_page(self):
		pass

	def get_ans_data(self):
		pass

	def parse_ans_data(self):
		pass
