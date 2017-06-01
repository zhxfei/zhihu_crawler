# -*- coding: utf-8 -*-

import scrapy
import json
from zhihu_spider.items import ZhihuUserItem,ZhihuUserItemLoader
from datetime import datetime


following_api = 'https://www.zhihu.com/api/v4/members/{}/followees?include=data%5B%2A%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0'
members_api = "https://www.zhihu.com/api/v4/members/{}?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccolumns_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge[%3F(type%3Dbest_answerer)].topics"


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = [following_api.format('teng-xun-ke-ji')]
    handle_httpstatus_list = [403]

    def parse(self, response):
        # if response.status == 403:
        #     yield scrapy.Request('https://www.zhihu.com/api/v4/anticrawl/captcha_appeal',
        #                                             headers=self.headers,callback=self.get_captcha)
        jsonresponse = json.loads(response.body_as_unicode())
        if jsonresponse['data']:
            for data in jsonresponse['data']:
                url_token = data['url_token']
                yield scrapy.Request(url=members_api.format(url_token),callback=self.parse_detail)
                yield scrapy.Request(url=following_api.format(url_token))
        if not jsonresponse['paging']['is_end']:
            yield scrapy.Request(url=jsonresponse['paging']['next'])

    def parse_detail(self,response):
        if response.status == 200:
            jsonresponse = json.loads(response.body_as_unicode())
            agreed_count = jsonresponse['voteup_count']
            thxd_count = jsonresponse['thanked_count']
            collected_count = jsonresponse['favorited_count']
            if thxd_count or collected_count:
                item_loader = ZhihuUserItemLoader(item=ZhihuUserItem(), response=response)
                item_loader.add_value('name',jsonresponse['name'])
                item_loader.add_value('id',jsonresponse['id'])
                item_loader.add_value('url_token',jsonresponse['url_token'])
                item_loader.add_value('headline',jsonresponse['headline']
                                                    if jsonresponse['headline'] else "无")
                item_loader.add_value('answer_count',jsonresponse['answer_count'])
                item_loader.add_value('articles_count',jsonresponse['articles_count'])
                item_loader.add_value('gender',jsonresponse['gender']
                                                    if jsonresponse['gender'] else 0)
                item_loader.add_value('avatar_url',jsonresponse['avatar_url_template'].format(size='xl'))
                item_loader.add_value('user_type',jsonresponse['user_type'])
                item_loader.add_value('badge',','.join([badge.get('description') for badge in jsonresponse['badge']])
                                                    if jsonresponse.get('badge') else "无")
                item_loader.add_value('follower_count',jsonresponse['follower_count'])
                item_loader.add_value('following_count',jsonresponse['following_count'])
                item_loader.add_value('agreed_count',agreed_count)
                item_loader.add_value('thxd_count',thxd_count)
                item_loader.add_value('collected_count',collected_count)
                item_loader.add_value('craw_time',datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                zhihu_item = item_loader.load_item()
                yield zhihu_item





# try:
#     from PIL import Image
# except:
#     pass



        # headers = {
        #     "Host": "www.zhihu.com",
        #     "Referer": "https://www.zhihu.com/",
        #     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0',
        #     'Upgrade-Insecure-Requests':'1'
        # }

        # postdata = {
        #     '_xsrf': '',
        #     'password': 'zhxfei..192',
        #     'phone_num': '15852937839',
        #     'captcha': ''
        # }


        # def start_requests(self):
        #     return [scrapy.Request('https://www.zhihu.com/#login',headers=self.headers,callback=self.get_xsrf)]
        #
        # def get_xsrf(self,response):
        #     response_text = response.text
        #     mathch_obj = re.match('.*name="_xsrf" value="(.*?)"',response_text,re.DOTALL)
        #     if mathch_obj:
        #         self.postdata['_xsrf'] =  mathch_obj.group(1)
        #         t = str(int(time.time() * 1000))
        #         captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
        #         return [scrapy.Request(captcha_url,headers=self.headers,callback=self.get_captcha)]
        #
        # def get_captcha(self,response):
        #     with open('captcha.jpg', 'wb') as f:
        #         f.write(response.body)
        #         f.close()
        #     try:
        #         im = Image.open('captcha.jpg')
        #         im.show()
        #         #im.close()
        #     except:
        #         print('find captcha by your self')
        #     self.postdata['captcha'] = input("please input the captcha\n>").strip()
        #     if self.postdata['_xsrf'] and self.postdata['captcha']:
        #         post_url = 'https://www.zhihu.com/login/phone_num'
        #         return [scrapy.FormRequest(
        #             url=post_url,
        #             formdata=self.postdata,
        #             headers=self.headers,
        #             callback=self.check_login
        #         )]
        #
        # def check_login(self,response):
        #     json_text = json.loads(response.text)
        #     if 'msg' in json_text and json_text['msg'] == '登录成功':
        #         for url in self.start_urls:
        #             yield scrapy.Request(url,headers=self.headers)  #no callback , turn into parse
        #

        # def start_requests(self):
        #     for url in self.start_urls:
        #         yield scrapy.Request(url, headers=self.headers)
        #
