""" Utility functions that both bots use. """
import json


def load_oauth_config(system):
    """
    Returns the OAuth configuration keys for the given system.

    Args:
        system (str) - which system is being used (i.e. 'tumblr' or 'twitter')

    Returns:
        a tuple of the form: (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    """
    with open('config.json', 'r') as config_file:
        config = json.load(config_file).get(system)
        return (
            config.get('consumer_key'), 
            config.get('consumer_secret'),
            config.get('access_token'), 
            config.get('access_token_secret')
        )


def load_blog_name():
    """
    Fetches the name of the Tumblr blog that we will be posting to.
    """
    with open('config.json', 'r') as config_file:
        config = json.load(config_file).get('tumblr')
        return config.get('blog_name')

