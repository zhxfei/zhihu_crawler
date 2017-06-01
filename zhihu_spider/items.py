# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from scrapy.item import Item,Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join,TakeFirst,MapCompose
import MySQLdb


# def get_agreed_num(info):
#     '''
#     :param info: '获得 21479 次赞同'
#     :return:    21579
#     '''
#     if info:
#         num = re.match(r'.*\s(\d*)\s.*',info)
#         return int(num.group(1))
#
# def get_thx_num(info):
#     '''
#     :param info: '获得 7702 次感谢，20686 次收藏'
#     :return:    7702
#     '''
#     if info:
#         num = re.findall('\d+',info)
#         return int(num[0])
#
# def get_collect_num(info):
#     '''
#     :param info:'获得 7702 次感谢，20686 次收藏'
#     :return:    20686
#     '''
#     if info:
#         num = re.findall('\d+',info)
#         return int(num[1])
#


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

    '''
        def get_insert_sql(self):
        insert_sql = """
            insert into zhihu_user VALUES(%s,%s,%s,%s,%d,%d,%d,%s,%s,%d,%d,%d,%d,%d,%s,%s)
            ON DUPLICATE KEY UPDATE craw_time=VALUES(craw_time) following_count=VALUES(following_count)
            follower_count=VALUES(follower_count) thxd_count=VALUES(thxd_count) agreed_count=VALUES(agreed_count)
            collected_count=VALUES(collected_count)
        """

        params = (
            self['name'],self['id'],self['url_token'],self['headline'],self['answer_count'],
            self['articles_count'],self['gender'],self['avatar_url'],self['user_type'],
            self['following_count'],self['follower_count'], self['thxd_count'],self['agreed_count'],
            self['collected_count'], self['badge'], self['craw_time']
        )

        return insert_sql,params

    '''




class ZhihuUserItemLoader(ItemLoader):
    default_output_processor = TakeFirst()



class UserItem(Item):
    class UserItem(Item):
        # define the fields for your item here like:
        id = Field()
        name = Field()
        avatar_url = Field()
        headline = Field()
        description = Field()
        url = Field()
        url_token = Field()
        gender = Field()
        cover_url = Field()
        type = Field()
        badge = Field()

        answer_count = Field()
        articles_count = Field()
        commercial_question_count = Field()
        favorite_count = Field()
        favorited_count = Field()
        follower_count = Field()
        following_columns_count = Field()
        following_count = Field()
        pins_count = Field()
        question_count = Field()
        thank_from_count = Field()
        thank_to_count = Field()
        thanked_count = Field()
        vote_from_count = Field()
        vote_to_count = Field()
        voteup_count = Field()
        following_favlists_count = Field()
        following_question_count = Field()
        following_topic_count = Field()
        marked_answers_count = Field()
        mutual_followees_count = Field()
        hosted_live_count = Field()
        participated_live_count = Field()

        locations = Field()
        educations = Field()
        employments = Field()