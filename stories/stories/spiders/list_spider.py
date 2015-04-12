import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from stories.items import StoryItem


def view_complete(value):
    return "{}?view_adult=true&view_full_work=true".format(value)


class ListSpider(CrawlSpider):
    name = "ao3"
    allowed_domains = ["archiveofourown.org"]

    #TODO: make this an argument of the spider
    start_urls = [
        "http://archiveofourown.org/tags/Blaine%20Anderson*s*Kurt%20Hummel/works?commit=Sort+and+Filter&page=75&utf8=%E2%9C%93&work_search[complete]=1&work_search[language_id]=&work_search[other_tag_names]=&work_search[query]=&work_search[rating_ids][]=13&work_search[sort_column]=word_count"
    ]

    rules = [
        Rule(LinkExtractor(allow=(r'works/[0-9]+\?view_adult=true&view_full_work=true'), process_value=view_complete), callback='parse_item')
    ]

    def strip_and_join(self, list_text):
        """ Strips out HTML tags and unwanted unicode and joins all the paragraphs into a single string. """
        text = " ".join(list_text)
        stripped_text = re.sub("<.*?>", "", text)
        return stripped_text

    def parse_item(self, response):
        item = StoryItem()
        item['title'] = response.xpath('//h2/text()').extract()
        item['author'] = response.xpath('//a[@rel="author"]/text()').extract()
        if response.xpath('//div[@class="chapter"]'):
            # handle multi-chapter story
            text = response.xpath('//div[@id="chapters"]/div[@class="chapter"]/div[@role="article"]/node()').extract()
        else:
            # single-chapter story
            text = response.xpath('//div[@id="chapters"]/div[@class="userstuff"]/node()').extract()

        item['text'] = self.strip_and_join(text)
        return item
