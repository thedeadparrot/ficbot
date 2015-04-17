""" Tumblr bot for posting things to Tumblr. """

import pytumblr

import util

oauth_config = util.load_oauth_config('tumblr')
blog_name = util.load_blog_name()
client = pytumblr.TumblrRestClient(*oauth_config)

client.create_text(blog_name, state="publish", body="Hello, World!")
