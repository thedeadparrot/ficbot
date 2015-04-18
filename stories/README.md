Scraping
========

[Scrapy](http://scrapy.org/), the library I'm using to scrape AO3 has a bunch of requirements that will need to be downloaded separately. I only know how to do this on Ubuntu. Sorry for anyone else who might be stuck. Google the error messages you get, which is how I fixed things for myself.

1. For Ubuntu, you'll want to run: `sudo apt-get install python-dev libssl-dev libffi-dev libxml2-dev libxslt1-dev`
2. Create a new virtualenv and run `pip install -r requirements.txt` to get the right version of Scrapy.
3. Decide which story list pages (tag pages, author works list, etc) on AO3 you would like to pull. It won't run through all the pages of a single tag, etc. You will have to list each page individually.
4. Fill in the urls to these pages in `stories/settings.py` under the heading `STORY_LIST_URLS`.
5. From the top level of the stories project run `scrapy crawl ao3` to pull down the stories. Any story that has not been successfully processed (couldn't read in the story data for whatever reason) will not be saved. Parsing irregular HTML pages is hard, yo.
6. On top of the stories that will be dumped into the `corpus` directory, the script will also populate `stories.json`, which contains most of the metadata information for the stories as well. It is not used for model generation, but it's there in case you want to see more about a particular story.
