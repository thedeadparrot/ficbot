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
    # Fill this in with tag page urls, for example:
    # "http://archiveofourown.org/tags/Teen%20Wolf%20%28TV%29/works",
    # "http://archiveofourown.org/tags/Stargate%20Atlantis/works"
]

# local settings
try:
    from local_settings import *
except ImportError:
    pass
