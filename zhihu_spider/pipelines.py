# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
import os.path
from scrapy import Request

class MysqlTwsitedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbpara=dict(
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


class HeadImageDownloadPipeline(object):
    def process_item(self,item,spider):
        path = '/home/zhxfei/workspace/zhihu_spider/zhihu_spider/headimage/'+ item.get('url_token')
        if not os.path.exists(path):
            yield Request(url=item.get('avatar_url'),meta={'path':path},callback=self.hendler)
        else:
            yield item

    def hendler(self,response):
        with open(response.meta['path'],'w+') as f:
            f.write(response.body)













