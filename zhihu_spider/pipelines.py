# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
import pymongo
import os.path
from scrapy import Request

class ZhihuSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


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
        return item

    def handle_error(self,failure):
        print(failure)

    def do_insert(self,cursor,item):
        item.get_insert_sql()
        # cursor.execute(insert_sql,params)


class MysqlInsertPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost','root','zhxfei..192','crawler',charset='utf8')

    def process_item(self, item, spider):
        try:
            with self.conn as cursor:
                insert_sql = '''
                    replace into zhihu_user1 values('{}','{}','{}','{}',{},{},{},'{}','{}',{},{},{},{},{},'{}','{}')
                    '''.format(item['name'], item['id'], item['url_token'], item['headline'], item['answer_count'],
                               item['articles_count'],item['gender'], item['avatar_url'], item['user_type'],
                               item['following_count'], item['follower_count'],item['thxd_count'],
                               item['agreed_count'],item['collected_count'], item['badge'], item['craw_time'])
                cursor.execute(insert_sql)
        except Exception as e:

            print(e)
        finally:
            return item


'''
class HeadImageDownloadPipeline(object):
    def process_item(self,item,spider):
        path = '/home/zhxfei/workspace/zhihu_spider/zhihu_spider/headimage/'+ item.get('url_token')
        if not os.path.exists(path):
            yield Request(url=item.get('avatar_url'),headers={
            "Host": "www.zhihu.com",
            "Referer": "https://www.zhihu.com/",
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Upgrade-Insecure-Requests':'1'
            },meta={'path':path},callback=self.hendler)
        else:
            yield item

    def hendler(self,response):
        with open(response.meta['path'],'w+') as f:
            f.write(response.body)
'''
















class MongoPipeline(object):
    collection_name = 'users'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].update({'url_token': item['url_token']}, {'$set': dict(item)}, True)
        return item