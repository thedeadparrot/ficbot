# -*- coding: utf-8 -*-

# Scrapy settings for stories project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'stories'

SPIDER_MODULES = ['stories.spiders']
NEWSPIDER_MODULE = 'stories.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'stories (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'stories.pipelines.StoreTextPipeline': 300,
}

CORPUS_DIRECTORY = '../corpus'
JSON_OUTPUT = 'stories.json'

STORY_LIST_URLS = [
    "http://archiveofourown.org/tags/Blaine%20Anderson*s*Kurt%20Hummel/works?commit=Sort+and+Filter&page=75&utf8=%E2%9C%93&work_search[complete]=1&work_search[language_id]=&work_search[other_tag_names]=&work_search[query]=&work_search[rating_ids][]=13&work_search[sort_column]=word_count"
]
