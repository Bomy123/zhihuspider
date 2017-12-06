from zhihuspider.items import ZhihuspiderItem
from zhihuspider.spiders.dao.dbTools import Db
from zhihuspider.spiders.config import Config
class Commons:
    cookie = None
    @staticmethod
    def commit_item(datatype=None, id=None, rid=None, title=None, author=None, content=None, url=None,
                    content_type=None):
        item = ZhihuspiderItem()
        item["table"] = datatype
        if Config.debug:
            print(item["table"])
        item["id"] = id
        item["rid"] = rid
        item["title"] = title
        item["author"] = author
        item["content"] = content
        item["content_type"] = content_type
        item["url"] = url
        db = Db.getinstance()
        db.commit(item)
        return item

    @staticmethod
    def setcookie(cookie):
        Commons.cookie = cookie
        print(Commons.cookie)

    @staticmethod
    def getcookie():
        print(123)
        return Commons.cookie


if __name__ == '__main__':
    Commons.setcookie("12333333")
    print(Commons.getcookie())
