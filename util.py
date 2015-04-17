""" Utility functions that both bots use. """
import json

def load_oauth_config(system):
    with open('config.json', 'r') as config_file:
        config = json.load(config_file).get(system)
        return (
            config.get('consumer_key'), 
            config.get('consumer_secret'),
            config.get('access_token'), 
            config.get('access_token_secret')
        )

def load_blog_name():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file).get('tumblr')
        return config.get('blog_name')

