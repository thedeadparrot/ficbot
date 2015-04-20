""" Common Bot interface for these bots and other bots to use. """
import json
from generator import generate_text


class NoConfigurationError(Exception):
    pass


class SocialMediaBot(object):
    """
    An abstract base class for running a Social Media Fic Bot.
    """
    NAME = ""  # the name of service to post to.

    def __init__(self, config_file='config.json'):
        try:
            with open(config_file, 'r') as read_file:
                # load the configuration for this particular bot
                config = json.load(read_file).get(self.NAME)
                if not config:
                    raise NoConfigurationError(
                        "Could not find configuration for {} in configuration file.".format(self.NAME)
                    )
                for attr in config:
                    # load all of the configuration options onto object fields
                    setattr(self, attr, config.get(attr))
        except IOError:
            raise NoConfigurationError("Configuration file {} not found.".format(config_file))

    @property
    def oauth_config(self):
        """
        Returns the OAuth configuration keys for the given bot.
        """
        return (
            self.consumer_key,
            self.consumer_secret,
            self.access_token,
            self.access_token_secret,
        )

    def generate_text(**kwargs):
        """ A thin wrapper for the subclasses to use. """
        return generate_text(kwargs)

    def post_update(self):
        """
        Post an update to the social media service.
        """
        raise NotImplementedError()
