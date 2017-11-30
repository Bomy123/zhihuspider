from zhihuspider.spiders.commons import Commons
from zhihuspider.spiders.config import Config
def QuestionPageParser:
	def get_default_ques_page(self,id,url):
		return [Request(url,headers = Config.headers,meta={"id",id},callback = self.parse_default_ques_page)]
	def parse_default_ques_page(self,response):
		description = response.xpath('//span[@class="RichText"]/text()')
		Commons.commit_item(datatype=Config.question_type,id = [response.meta["id"]],content = description)
