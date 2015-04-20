""" Test the utility methods. """

import unittest
import util


class TestSocialMediaBot(unittest.TestCase):
    def setUp(self):
        self.bot = util.SocialMediaBot('tests/config_test.json')

    def test_initialization(self):
        self.assertEqual(self.bot.other_test_field, "I am a test field.")

    def test_oath_config(self):
        self.assertEqual(self.bot.oauth_config,
                         ("REPLACE ME", "REPLACE ME", "REPLACE ME", "REPLACE ME"))
