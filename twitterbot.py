from __future__ import print_function

from twython import Twython

import util

oauth_config = util.load_oauth_config('twitter')
twitter = Twython(*oauth_config)
twitter.update_status(status='hello, world!')
