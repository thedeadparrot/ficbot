# -*- coding: utf-8 -*-

import re
import json
import os
from stories import settings
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class StoreTextPipeline(object):
    """ This pipeline is responsible for writing out the text into a text file. """
    def __init__(self):
        self.json_file = open(settings.JSON_OUTPUT, 'wb')

    def process_item(self, item, spider):
        """
        Dumps item text into separate files and stores a json mapping
        between the stories and their titles/authors.
        """
        # create directory if it doesn't already exist
        directory = settings.CORPUS_DIRECTORY
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
