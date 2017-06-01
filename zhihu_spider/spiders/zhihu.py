# -*- coding: utf-8 -*-

import scrapy
import json
from zhihu_spider.items import ZhihuUserItem,ZhihuUserItemLoader
from datetime import datetime


following_api = "https://www.zhihu.com/api/v4/members/{}/followees?include=data[*].gender%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Canswer_count%2Carticles_count%2Cfavorite_count%2Cfavorited_count%2Cthanked_count%2Cbadge[%3F(type%3Dbest_answerer)].topics&offset=0&limit=20"

class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = [following_api.format('teng-xun-ke-ji')]
    handle_httpstatus_list = [403]

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())

        if not jsonresponse['paging']['is_end']:
            yield scrapy.Request(url=jsonresponse['paging']['next'])

        if jsonresponse['data']:
            for data in jsonresponse['data']:
                url_token = data.get('url_token')
                if url_token:
                    yield scrapy.Request(url=following_api.format(url_token))

                    agreed_count = data['voteup_count']
                    thxd_count = data['thanked_count']
                    collected_count = data['favorited_count']
                    if thxd_count or collected_count:
                        item_loader = ZhihuUserItemLoader(item=ZhihuUserItem(), response=response)
                        item_loader.add_value('name',data['name'])
                        item_loader.add_value('id',data['id'])
                        item_loader.add_value('url_token',data['url_token'])
                        item_loader.add_value('headline',data['headline']
                                                            if data['headline'] else "无")
                        item_loader.add_value('answer_count',data['answer_count'])
                        item_loader.add_value('articles_count',data['articles_count'])
                        item_loader.add_value('gender',data['gender']
                                                            if data['gender'] else 0)
                        item_loader.add_value('avatar_url',data['avatar_url_template'].format(size='xl'))
                        item_loader.add_value('user_type',data['user_type'])
                        item_loader.add_value('badge',','.join([badge.get('description') for badge in data['badge']])
                                                            if data.get('badge') else "无")
                        item_loader.add_value('follower_count',data['follower_count'])
                        item_loader.add_value('following_count',data['following_count'])
                        item_loader.add_value('agreed_count',agreed_count)
                        item_loader.add_value('thxd_count',thxd_count)
                        item_loader.add_value('collected_count',collected_count)
                        item_loader.add_value('craw_time',datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        zhihu_item = item_loader.load_item()
                        yield zhihu_item

