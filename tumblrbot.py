""" Tumblr bot for posting things to Tumblr. """

import pytumblr
import util


class TumblrBot(util.SocialMediaBot):
    """ Social Media Bot for posting updates to Tumblr """
    NAME = "tumblr"

    def __init__(self):
        super(TumblrBot, self).__init__(self)
        self.client = pytumblr.TumblrRestClient(*self.oauth_config)

    def post_update(self):
        text = self.generate_text(num_words=400)
        self.client.create_text(self.blog_name, state='publish', body=text)

tumblrbot = TumblrBot()
tumblrbot.post_update()
