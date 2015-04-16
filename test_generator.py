""" Tests for generating the model. """

import unittest
import nltk
import random
import six

from generator import conditional_ngrams, conditional_bigrams, conditional_trigrams, get_random_choice, generate_sequence


class TestConditionalGeneration(unittest.TestCase):
    """ Test the conditional format generation. """
    TEST_CORPUS = "The brown dog jumped."

    def test_conditional_bigrams(self):
        bigrams = conditional_bigrams(nltk.bigrams(nltk.word_tokenize(self.TEST_CORPUS)))
        self.assertEqual(list(bigrams), [(('The',), 'brown'), (('brown',), 'dog'), (('dog',), 'jumped'), (('jumped',), '.')])

    def test_conditional_trigrams(self):
        trigrams = conditional_trigrams(nltk.trigrams(nltk.word_tokenize(self.TEST_CORPUS)))
        self.assertEqual(list(trigrams), [(('The', 'brown'), 'dog'), (('brown', 'dog'), 'jumped'), (('dog', 'jumped'), '.')])

    def test_conditional_ngram_2(self):
        bigrams = conditional_bigrams(nltk.bigrams(nltk.word_tokenize(self.TEST_CORPUS)))
        ngrams = conditional_ngrams(nltk.ngrams(nltk.word_tokenize(self.TEST_CORPUS), 2), 2)
        self.assertEqual(list(bigrams), list(ngrams))

    def test_conditional_ngram_3(self):
        trigrams = conditional_trigrams(nltk.trigrams(nltk.word_tokenize(self.TEST_CORPUS)))
        ngrams = conditional_ngrams(nltk.ngrams(nltk.word_tokenize(self.TEST_CORPUS), 3), 3)
        self.assertEqual(list(trigrams), list(ngrams))



class TestSequenceGeneration(unittest.TestCase):
    """ Test Sequence Generation. """
    
    TEST_CORPUS = 'abbabacd'
    def setUp(self):
        random.seed(1)
        # generate dist for TEST_CORPUS
        self.cfd = nltk.ConditionalFreqDist(conditional_bigrams(nltk.bigrams(self.TEST_CORPUS)))

    def test_get_random_word(self):
        word = get_random_choice(self.cfd[('a',)])
        self.assertEqual(word, 'b')

    def test_generate_sequence(self):
        generated = generate_sequence(self.cfd, ('a',), 6)
        # Python 3 changed its seeding method, so the sequence we get is different
        if six.PY2:
            expected = list('abbbaba')
        elif six.PY3:
            expected = list('ababacd')
        self.assertEqual(generated, expected)
