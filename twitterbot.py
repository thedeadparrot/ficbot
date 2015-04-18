from __future__ import print_function

from twython import Twython

import util
from generator import generate_text

text = generate_text(limit_characters=140)
oauth_config = util.load_oauth_config('twitter')
twitter = Twython(*oauth_config)
twitter.update_status(status=text)
