# -*- coding: utf-8 -*-

import re
import json
import os
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class StoreTextPipeline(object):
    """ This pipeline is responsible for writing out the text into a text file. """
    def __init__(self):
        self.json_file = open('stories.json', 'wb')

    def process_item(self, item, spider):
        # create directory if it doesn't already exist
        directory = 'corpus'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # strip useless characters from the filename
        filename = "".join(c for c in item['title'] if re.match(r'\w', c))
        full_file = "{}/{}.txt".format(directory, filename)
        with open(full_file, 'wb') as text_file:
            text_file.write(item['text'])

        # write information into a helpful JSON file
        item_fields = dict(item)
        item_fields['text'] = full_file
        self.json_file.write(json.dumps(item_fields) + '\n')

        return item
