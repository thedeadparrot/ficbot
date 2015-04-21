""" Testing the bots to make sure they work. """

import unittest
import mock
from twitterbot import TwitterBot
from tumblrbot import TumblrBot


class TestTwitterBot(unittest.TestCase):
    def setUp(self):
        self.bot = TwitterBot(config_file='tests/config_test.json')

    def test_oath_config(self):
        self.assertEqual(self.bot.oauth_config,
                         ("REPLACE ME", "REPLACE ME", "REPLACE ME", "REPLACE ME"))

    @mock.patch('util.generate_text', return_value='hello')
    @mock.patch('twython.Twython.update_status')
    def test_update_status(self, update_status_mock, generate_text_mock):
        self.bot.post_update()
        generate_text_mock.assert_called_with(limit_characters=140)
        update_status_mock.assert_called_with(status='hello')


class TestTumblrBot(unittest.TestCase):
    def setUp(self):
        self.bot = TumblrBot(config_file='tests/config_test.json')

    def test_initialization(self):
        self.assertEqual(self.bot.oauth_config,
                         ("REPLACE ME", "REPLACE ME", "REPLACE ME", "REPLACE ME"))
        self.assertEqual(self.bot.blog_name, "fake blog name")

    @mock.patch('util.generate_text', return_value='hello')
    @mock.patch('pytumblr.TumblrRestClient.create_text')
    def test_update_status(self, create_text_mock, generate_text_mock):
        self.bot.post_update()
        generate_text_mock.assert_called_with(num_words=400)
        create_text_mock.assert_called_with(self.bot.blog_name, state='publish', body='hello')
