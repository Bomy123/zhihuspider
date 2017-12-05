from zhihuspider.items import ZhihuspiderItem
from zhihuspider.spiders.config import Config
from zhihuspider.spiders.interface import IDbTools
import logging
import pymysql


class Db(IDbTools):
    conn = None
    mdict = {}
    minstance = None

    def __init__(self):
        super().__init__()
        self.conn = pymysql.connect(host=Config.db_host, port=Config.db_port, user=Config.db_user,
                                    password=Config.db_passwd, database=Config.db_name, charset=Config.charset)

    # @staticmethod
    # def getinstance():
    #     if DbUtils.minstance is None:
    #         DbUtils.minstance = DbUtils()
    #     return DbUtils.minstance

    def commit(self, item: ZhihuspiderItem):
        try:
            if item["table"] is None:
                return False
            else:
                self.mdict[item["table"][0]](item)
        except Exception as e:
            print("KeyError:", e)

    def _register(self):
        print("注册方法")
        self.mdict[Config.topics_type[0]] = self.__tinsert
        self.mdict[Config.artical_type[0]] = self.__ainsert
        self.mdict[Config.class_type[0]] = self.__cinsert
        self.mdict[Config.question_type[0]] = self.__qinsert
        self.mdict[Config.answer_type[0]] = self.__aninsert
        self.mdict[Config.profession_type[0]] = self.__pinsert

    def addmethod(self, mkey=None, m=None):
        if mkey is None or m is None:
            logging.error(msg="key or method is None")
            return False
        if self.mdict.get(mkey, -1) is not -1:
            logging.error(msg="key 已经被注册，请修改key后重新注册")
            return False
        self.mdict[mkey] = m
        return True

    def __tinsert(self, item):
        for idx in range(0,len(item["id"])):
            sql = self.composql("topics",item["title"][idx],item["id"][idx],item["url"][idx])
            if Config.debug:
                print(sql)
            self.conn.query(sql=sql)
            self.conn.commit()

    def __cinsert(self, item):
        for idx in range(0,len(item["id"])):
            sql = self.composql("class",item["title"][idx],item["id"][idx],item["url"][idx],item["rid"][0])
            if Config.debug:
                print(sql)
            self.conn.query(sql=sql)
            self.conn.commit()

    def __ainsert(self, item):
        for idx in range(0,len(item["id"])):
            sql = self.composql("artical",item["title"][idx],item["id"][idx],item["content_type"][idx],item["url"][idx],item["rid"][0])
            if Config.debug:
                print(sql)
            self.conn.query(sql=sql)
            self.conn.commit()

    def __qinsert(self, item):
        for idx in range(0,len(item["id"])):
            sql = self.composql("question",item["content"][idx],item["id"][idx])
            self.conn.query(sql=sql)
            self.conn.commit()

    def __aninsert(self, item):
        for idx in range(0,len(item["id"])):
            sql = self.composql("class",item["content"][idx],item["author"][idx],item["id"][idx],item["rid"][0])
            if Config.debug:
                print(sql)
            self.conn.query(sql=sql)
            self.conn.commit()

    def __pinsert(self, item):
        for idx in range(0,len(item["id"])):
            sql = self.composql("special",item["content"][idx],item["id"][idx])
            if Config.debug:
                print(sql)
            self.conn.query(sql=sql)
            self.conn.commit()

    def composql(self,table,*args):
        sql = "INSERT INTO topics VALUES(null,"
        for i in range(0,len(args)-1):
            sql += "'"+args[i] + "',"
        sql += "'"+args[len(args)-1]+"')"
        return sql

    def __del__(self):
        try:
            self.conn.close()
        except Exception as e:
            print(e.__str__())


if __name__ == '__main__':
    du = Db()
