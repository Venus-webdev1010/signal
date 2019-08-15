# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class SignalProjectPipeline(object):

    def __init__(self):
        self.church_seen = set()

    def process_item(self, item, spider):
        churchid = (item['page_url'] if item['page_url'] else '')
        if churchid in self.church_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.church_seen.add(churchid)
            return item

