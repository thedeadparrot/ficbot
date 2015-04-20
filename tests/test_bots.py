""" Testing the bots to make sure they work. """

import unittest
from twitterbot import TwitterBot
from tumblrbot import TumblrBot


class TestTwitterBot(unittest.TestCase):
    def setUp(self):
        self.bot = TwitterBot(config_file='tests/config_test.json')

    def test_oath_config(self):
        self.assertEqual(self.bot.oauth_config,
                         ("REPLACE ME", "REPLACE ME", "REPLACE ME", "REPLACE ME"))


class TestTumblrBot(unittest.TestCase):
    def setUp(self):
        self.bot = TumblrBot(config_file='tests/config_test.json')

    def test_initialization(self):
        self.assertEqual(self.bot.oauth_config,
                         ("REPLACE ME", "REPLACE ME", "REPLACE ME", "REPLACE ME"))
        self.assertEqual(self.bot.blog_name, "fake blog name")
