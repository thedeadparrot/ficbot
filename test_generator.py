""" Tests for generating the model. """

import unittest
import nltk

from generator import conditional_bigrams, conditional_trigrams


class TestConditionalGeneration(unittest.TestCase):
    TEST_CORPUS = "The brown dog jumped."

    def test_conditional_bigrams(self):
        bigrams = conditional_bigrams(nltk.bigrams(nltk.word_tokenize(self.TEST_CORPUS)))
        self.assertEquals(list(bigrams), [(('The',), 'brown'), (('brown',), 'dog'), (('dog',), 'jumped'), (('jumped',), '.')])

    def test_conditional_trigrams(self):
        trigrams = conditional_trigrams(nltk.trigrams(nltk.word_tokenize(self.TEST_CORPUS)))
        self.assertEquals(list(trigrams), [(('The', 'brown'), 'dog'), (('brown', 'dog'), 'jumped'), (('dog', 'jumped'), '.')])

