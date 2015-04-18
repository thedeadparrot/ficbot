""" Tumblr bot for posting things to Tumblr. """

import pytumblr

import util
from generator import generate_text

text = generate_text(num_words=500)
oauth_config = util.load_oauth_config('tumblr')
blog_name = util.load_blog_name()
client = pytumblr.TumblrRestClient(*oauth_config)

client.create_text(blog_name, state="publish", body=text)
