# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class MysqlTwsitedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbpara = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_NAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASS'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb",**dbpara)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)
        yield item

    def handle_error(self,failure):
        print(failure)

    def do_insert(self,cursor,item):
        insert_sql = item.get_insert_sql()
        cursor.execute(insert_sql)
