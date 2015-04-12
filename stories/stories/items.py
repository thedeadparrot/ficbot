# -*- coding: utf-8 -*-
""" Models that represents a stories that has been scraped. """
import scrapy


class StoryItem(scrapy.Item):
    """ Item that represents a story. """
    title = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field()
    language = scrapy.Field()
    rating = scrapy.Field()
    warning = scrapy.Field()
    category = scrapy.Field()
    fandom = scrapy.Field()
    relationship = scrapy.Field()
    character = scrapy.Field()
