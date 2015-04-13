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

    def strip_and_join(self, list_text, separator=" "):
        """ Strips out HTML tags and unwanted unicode and joins all the paragraphs into a single string. """
        text = separator.join(list_text).strip()
        stripped_text = re.sub("<.*?>", "", text)
        # force unicode into closest possible ASCII
        decoded_text = unidecode(stripped_text)
        return decoded_text

    def parse_tags(self, response, item, tag_category):
        xpath = '//dd[@class="{} tags"]/ul/li/a/text()'.format(tag_category)
        item[tag_category] = response.xpath(xpath).extract()

    def parse_item(self, response):
        """ On the individual story pages, parse the page and save relevant data. """
        item = StoryItem()
        item['title'] = self.strip_and_join(response.xpath('//h2/text()').extract())
        item['author'] = self.strip_and_join(response.xpath('//a[@rel="author"]/text()').extract(), separator=", ")
        # handle tags
        for category in ["rating", "warning", "category", "fandom", "relationship", "character"]:
            self.parse_tags(response, item, category)

        item['language'] = self.strip_and_join(response.xpath('//dd[@class="language"]/text()').extract())

        if response.xpath('//div[@class="chapter"]'):
            # handle multi-chapter story
            text = response.xpath('//div[@id="chapters"]/div[@class="chapter"]/div[@role="article"]/p/text()').extract()
        else:
            # single-chapter story
            text = response.xpath('//div[@id="chapters"]/div[@class="userstuff"]/p/text()').extract()

        item['text'] = self.strip_and_join(text, "\n\n")
        return item
