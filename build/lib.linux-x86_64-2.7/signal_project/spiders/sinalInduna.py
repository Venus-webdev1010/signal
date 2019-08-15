# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from signal_project.items import SignalProjectItem
import time, datetime, csv, random, base64, re, json
from time import sleep
import os
import os.path
from scrapy.selector import Selector
import sys
import re

class SinalindunaSpider(scrapy.Spider):
    name = 'sinalInduna'
    allowed_domains = ['www.signal-iduna.de']
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        
    }

    start_urls = ['http://www.signal-iduna.de/']

    # def parse(self, response):
    #     pass
    def start_requests(self):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        url_list = ['{}{}%'.format(first_letter, second_letter) for first_letter in letters for second_letter in letters]
        for param in url_list:
            url = "https://www.signal-iduna.de/adp-suche?singleSearch={}".format(param)
            req = Request(url=url, callback=self.get_list, headers=self.headers, dont_filter=True)
            yield req
            # return
    def get_list(self, response):
        
        result_list = response.xpath('//h2[contains(@class, "heading-primary")]')
        if result_list != '':
            for result in result_list:
                url = response.urljoin(result.xpath('./a/@href').extract_first())
                # url = 'https://www.signal-iduna.de/christian.harzer'
                req = Request(url=url, callback=self.parse_information, headers=self.headers, dont_filter=True)
                yield req 
                # return

        next_link = response.xpath('//ul[@class="pagination"]/li/a[@rel = "next"]/@href').extract_first('')
        if next_link != '':
            req = Request(url=response.urljoin(next_link), callback=self.get_list, headers=self.headers, dont_filter=True)
            yield req
        #     return 

    
    def parse_information(self, response):
        
        # print('================>', response.url)
        page_url = response.url
        # print '--- parse_shop ---'
        item = SignalProjectItem()
        try:
            first_name = response.xpath('//h3[@class="text-big"]/span[@class="hide767"]/text()').extract_first().strip()
            last_name = response.xpath('//h3[@class="text-big"]/span[@class="adp_name"]/text()').extract_first().strip()
            street_number = response.xpath('//p[@class="adressinfo"]/text()').extract()[0].split('\n')
            street_number = ' '.join([s.strip() for s in street_number])
            post_code = response.xpath('//p[@class="adressinfo"]/text()').extract()[1].split('\n')
            post_code = ' '.join([s.strip() for s in post_code])
        except Exception as e:
            print(e)
            first_name = ''
            last_name = ''
            street_number = ''
            post_code = ''
        try:
            phone = ''
            Mobile = ''
            Fax = ''
            person_element = response.xpath('//p[@class="telefonnummern"]/text()').extract()
            for person in person_element:
                # print (person)
                # print("person=====", person)
                if 'tel' in person.lower():
                    phone = re.sub(r"[^\d]", "", person)
                    phone = phone.zfill(11)
                    phone = phone[0:4] + ' ' + phone[4:]
                    # phone = "'" + person.split(':')[-1].strip()
                elif 'fax' in person.lower():
                    # Fax = person.split(':')[-1].strip()
                    Fax = re.sub(r"[^\d]", "", person)
                    Fax = Fax.zfill(11)
                    Fax = Fax[0:4] + ' ' + Fax[4:]
                elif 'mobil' in person.lower():
                    # Mobile = person.split(':')[-1].strip()
                    Mobile = re.sub(r"[^\d]", "", person)
                    Mobile = Mobile.zfill(11)
                    Mobile = Mobile[0:4] + ' ' + Mobile[4:]
                else:
                    pass
        
        except Exception as e:
            print(e)
            phone = ''
            Fax = ''
            Mobile = ''   
        try:
            register_name = response.xpath('//strong[contains(text(), "Registerabruf:")]/following-sibling::strong[1]/text()').extract_first().strip()
        except Exception as e:
            print(e)
            register_name = ''
        item['page_url'] = page_url 
        item["first_name"] = first_name
        item["last_name"] = last_name
        item["street_number"] = street_number
        item["post_code"] = post_code
        item["phone"] = phone
        item["Fax"] = Fax
        item["Mobile"] = Mobile
        item["register_name"] = register_name

        print('first_name=',first_name)
        print('last_name=',last_name)
        print('street_number=',street_number)
        print('post_code=',post_code)
        print('pone_number=',phone)
        print('Fax=', Fax)
        print('Mobile=', Mobile)
        print('register_name=', register_name)

        yield item
