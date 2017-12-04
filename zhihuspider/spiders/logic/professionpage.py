import re
import time
import random
from scrapy.http import Request
from scrapy.http import FormRequest
from zhihuspider.spiders.config import Config
from zhihuspider.spiders.commons import Commons


class ProfesionPageParser:
    def get_default_pro_data(self, id, url):
        return [Request(url, headers=Config.headers, meta={"id": [id]}, callback=self.parse_default_pro_page)]

    def parse_default_pro_page(self, response):
        author = response.xpath("").extract()
        contents = response.xpath("").extract()
        Commons.commit_item(datatype=Config.profession_type, id=response.meta["id"], author=author, content=contents)
