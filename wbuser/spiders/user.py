# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Request
import re
from wbuser.items import WbuserItem



class UserSpider(scrapy.Spider):
    name = 'user'
    allowed_domains = ['https://m.weibo.cn']
    Cookies = {'_T_WM': '7cf6b2c8e2f6a7c29c47cbf40fb42745',
               'SCF': 'AnapK-SAzpgzXF6sGyW2Q8C0scS24BOU55tfqMLEjzGK1xTGR9fSmTct_3SKFaVwFx3VqRfV9oqC-3s4467ghNw.',
               'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh4BuoILiJbnID6r-TL0Z3k5JpX5o2p5NHD95Qfeoz41Kz7Sh20Ws4Dqcj_i--Ni-8hiK.pi--Ni-8hiK.pi--Xi-zRiKy2i--NiKLsi-2fi--4iKnpiK.0',
               ' SUB': '_2A250vPmHDeRhGeNM6VsY8i7Iyj-IHXVUXofPrDV6PUJbkdBeLVHVkW099FMwszYrfQHgt1QqFmefQF_OuA..',
               ' SUHB': '0U1552VNEAl3fZ',
               'SSOLoginState': '1505266135',
               'H5_INDEX': '0_all',
               'H5_INDEX_TITLE': '%E7%AC%91%E7%AC%91%E4%B8%8D%E7%9F%A5%E9%81%93',
               'M_WEIBOCN_PARAMS': 'luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E9%259D%25B3%25E4%25B8%259C%26featurecode%3D20000320%26fid%3D1076031093897112%26uicode%3D10000011'}
    url='https://m.weibo.cn/api/container/getIndex?uid=1093897112&luicode=10000011&lfid=100103type%3D1%26q%3D%E9%9D%B3%E4%B8%9C&featurecode=20000320&type=uid&value=1093897112&containerid=1076031093897112&page={page}'



    def start_requests(self):
        url='https://m.weibo.cn/api/container/getIndex?uid=1093897112&luicode=10000011&lfid=100103type%3D1%26q%3D%E9%9D%B3%E4%B8%9C&featurecode=20000320&type=uid&value=1093897112&containerid=1076031093897112'
        yield Request(url=url,cookies=self.Cookies,callback=self.parseindex)
        yield Request(url=url, cookies=self.Cookies, callback=self.parse,dont_filter=True)



    def parse(self, response):
        html=json.loads(response.text)
        page=html['cardlistInfo']['total']//10+2
        for i in range(2,int(page)):
            yield Request(url=self.url.format(page=i),cookies=self.Cookies,callback=self.parseindex,dont_filter=True)



    def parseindex(self,response):
        html = json.loads(response.text)
        cards = html['cards']
        for card in cards :
            if card['card_type']==9:
                id=card['mblog']['id']
                url='https://m.weibo.cn/status/'+id
                # print(url)
                yield Request(url=url,cookies=self.Cookies,callback=self.parse2,dont_filter=True)
            else:
                pass


    def parse2(self,response):
        #有两种方式parse，1.通过网页提取源码text，在https://m.weibo.cn/api/comments/show?id=4149334088060486&page=1 中提取评论，
        # 2通过https://m.weibo.cn/statuses/extend?id=4149334088060486 中提取text，在https://m.weibo.cn/api/comments/show?id=4149334088060486&page=1
        #中提取评论,第二种没发现内容发布时间端口

        html=response.text
        pattern1=re.compile('.*?"created_at":(.*?)"id":',re.S)
        pattern2=re.compile('.*?"text":(.*?)"textLength":',re.S)
        pattern3=re.compile('.*?"reposts_count":(.*?)"comments_count":',re.S)
        pattern4 = re.compile('.*?"comments_count":(.*?)"attitudes_count":', re.S)
        pattern5 = re.compile('.*?"attitudes_count":(.*?)"isLongText":', re.S)
        pattern6 = re.compile('.*?"id":(.*?)"mid":', re.S)

        time = re.findall(pattern1, html)[0]#发布时间
        text=re.findall(pattern2,html)#内容
        reposts_count=re.findall(pattern3,html)[0][1:-9]#转发
        comments_count=re.findall(pattern4,html)[0][1:-9]#评论
        attitudes_count=re.findall(pattern5,html)[0][1:-9]#点赞
        id=re.findall(pattern6,html)[0][2:-11]    # "4149334088060486",
        # url='https://m.weibo.cn/api/comments/show?id={id}&page=1'.format(id=id)#评论内容json api
        if text:
            item=WbuserItem()
            for field in item.fields:
                try:
                    item[field]=eval(field)
                except NameError:
                    print('field is Not Defind',field)
            yield item
        else:
            pattern9 = re.compile('.*?"text":(.*?)"source":', re.S)
            text = re.findall(pattern9, html)  # 内容
            item = WbuserItem()
            for field in item.fields:
                try:
                    item[field] = eval(field)
                except NameError:
                    print('field is Not Defind', field)
            yield item







