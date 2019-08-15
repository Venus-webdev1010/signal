# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SignalProjectItem(scrapy.Item):
   
    first_name = scrapy.Field()   
    last_name = scrapy.Field()    
    street_number = scrapy.Field()
    post_code = scrapy.Field()    
    phone = scrapy.Field()
    Fax = scrapy.Field()
    Mobile = scrapy.Field()    
    register_name = scrapy.Field()
    page_url = scrapy.Field()
