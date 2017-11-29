from zhihuspider.items import ZhihuspiderItem
from zhihuspider.spiders.dao.dbTools import Db


class Commons:
    def commit_item(datatype=None,id = None,rid = None,title = None,author = None,content = None,url=None):
        item = ZhihuspiderItem()
        item["type"] = datatype
        item["id"] = id
        item["rid"] = rid
        item["title"] = title
        item["author"] = author
        item["content"] = content
        item["url"] = url
        db = Db.getinstance()
        db.commit(item)
        return item
