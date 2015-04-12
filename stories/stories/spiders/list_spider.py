import re
from unidecode import unidecode

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from stories import settings
from stories.items import StoryItem


def view_complete(value):
    """ Append necessary request values onto the url. """
    return "{}?view_adult=true&view_full_work=true".format(value)


class ListSpider(CrawlSpider):
    """
    For parsing tag list pages on AO3 and scraping the data of individual works.
    """
    name = "ao3"
    allowed_domains = ["archiveofourown.org"]

    start_urls = settings.STORY_LIST_URLS

    rules = [
        Rule(LinkExtractor(allow=(r'works/[0-9]+\?view_adult=true&view_full_work=true'), process_value=view_complete), callback='parse_item')
    ]

    def __itit__(self, *args, **kwargs):
        super(ListSpider, self).__init__(*args, **kwargs)

    def strip_and_join(self, list_text):
        """ Strips out HTML tags and unwanted unicode and joins all the paragraphs into a single string. """
        text = " ".join(list_text).strip()
        stripped_text = re.sub("<.*?>", "", text)
        # force unicode into closest possible ASCII
        decoded_text = unidecode(stripped_text)
        return decoded_text

    def parse_item(self, response):
        """ On the individual story pages, parse the page and save relevant data. """
        item = StoryItem()
        item['title'] = self.strip_and_join(response.xpath('//h2/text()').extract())
        item['author'] = self.strip_and_join(response.xpath('//a[@rel="author"]/text()').extract())
        #TODO: add new fields for tags (fandom, pairing, freeform, etc.)
        if response.xpath('//div[@class="chapter"]'):
            # handle multi-chapter story
            text = response.xpath('//div[@id="chapters"]/div[@class="chapter"]/div[@role="article"]/node()').extract()
        else:
            # single-chapter story
            text = response.xpath('//div[@id="chapters"]/div[@class="userstuff"]/node()').extract()

        item['text'] = self.strip_and_join(text)
        return item
