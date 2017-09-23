# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class WbuserItem(scrapy.Item):

    table_name='wbuser'
    time= scrapy.Field()
    text= scrapy.Field()
    id= scrapy.Field()
    reposts_count = scrapy.Field()
    comments_count = scrapy.Field()
    attitudes_count =scrapy.Field()