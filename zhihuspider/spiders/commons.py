from zhihuspider.items import ZhihuspiderItem
from zhihuspider.spiders.dao.dbTools import Db


class Commons:
	__cookie = None
    def commit_item(datatype=None,id = None,rid = None,title = None,author = None,content = None,url=None,content_type = None):
        item = ZhihuspiderItem()
        item["table"] = datatype
        item["id"] = id
        item["rid"] = rid
        item["title"] = title
        item["author"] = author
        item["content"] = content
		item["content_type"] = content
        item["url"] = url
        db = Db.getinstance()
        db.commit(item)
        return item

	def setcookie(cookie):
		__cookie = cookie
		print(__cookie)

	def getcookie(cookie):
		return __cookie
