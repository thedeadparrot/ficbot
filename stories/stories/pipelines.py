# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class StoriesPipeline(object):
    def process_item(self, item, spider):

        # dump text to a file

        # construct json that points to file name
        return item
