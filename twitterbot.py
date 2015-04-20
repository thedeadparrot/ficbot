from __future__ import print_function

from twython import Twython
import util


class TwitterBot(util.SocialMediaBot):
    """ Social Media Bot for posting updates to Tumblr """
    NAME = "twitter"

    def __init__(self, **kwargs):
        super(TwitterBot, self).__init__(**kwargs)
        self.client = Twython(*self.oauth_config)

    def post_update(self):
        text = self.generate_text(limit_characters=140)
        self.client.update_status(status=text)

if __name__  == "__main__":
    twitterbot = TwitterBot()
    twitterbot.post_update()
