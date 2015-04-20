from __future__ import print_function

from twython import Twython
import util


class TwitterBot(util.SocialMediaBot):
    """ Social Media Bot for posting updates to Tumblr """
    NAME = "twitter"

    def __init__(self):
        super(TwitterBot, self).__init__(self)
        self.client = Twython(*self.oauth_config)

    def post_update(self):
        text = self.generate_text(limit_characters=140)
        self.client.update_status(status=text)

twitterbot = TwitterBot()
twitterbot.post_update()
