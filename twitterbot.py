from __future__ import print_function

import json
from twython import Twython


with open('config.json', 'r') as config_file:
    config = json.load(config_file).get('twitter')
    twitter = Twython(
        config.get('consumer_key'), 
        config.get('consumer_secret'),
        config.get('access_token'), 
        config.get('access_token_secret')
    )
    twitter.update_status(status='hello, world!')
