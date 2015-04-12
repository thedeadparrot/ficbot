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

CORPUS_DIRECTORY = '../corpus'

ITEM_PIPELINES = {
    'stories.pipelines.StoreTextPipeline': 300,
}
