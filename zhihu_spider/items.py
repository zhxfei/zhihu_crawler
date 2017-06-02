# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join,TakeFirst,MapCompose



class ZhihuUserItem(Item):
    name = scrapy.Field()
    id = scrapy.Field()
    url_token = scrapy.Field()
    headline = scrapy.Field()
    answer_count = scrapy.Field()
    articles_count = scrapy.Field()
    gender = scrapy.Field()
    avatar_url = scrapy.Field()
    user_type = scrapy.Field()
    following_count = scrapy.Field()
    follower_count = scrapy.Field()
    thxd_count = scrapy.Field()
    agreed_count = scrapy.Field()
    collected_count = scrapy.Field()
    badge = scrapy.Field()
    craw_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = '''
            replace into zhihu_user_info values('{}','{}','{}','{}',{},{},{},'{}','{}',{},{},{},{},{},'{}','{}')
            '''.format(self['name'], self['id'], self['url_token'], self['headline'], self['answer_count'],
                       self['articles_count'], self['gender'], self['avatar_url'], self['user_type'],
                       self['following_count'], self['follower_count'], self['thxd_count'],
                       self['agreed_count'], self['collected_count'], self['badge'], self['craw_time'])

        return insert_sql





class ZhihuUserItemLoader(ItemLoader):
    default_output_processor = TakeFirst()



