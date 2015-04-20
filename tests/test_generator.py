""" Tests for generating the model. """

import unittest
import random

import nltk
import six

from generator import (conditional_ngrams, conditional_bigrams, conditional_trigrams,
                       get_random_choice, generate_sequence, clean_text, sentence_starts)


class TestConditionalGeneration(unittest.TestCase):
    """ Test the conditional format generation. """
    TEST_CORPUS = "The brown dog jumped."

    def test_conditional_bigrams(self):
        bigrams = conditional_bigrams(nltk.bigrams(nltk.word_tokenize(self.TEST_CORPUS)))
        self.assertEqual(
            list(bigrams),
            [(('The',), 'brown'), (('brown',), 'dog'), (('dog',), 'jumped'), (('jumped',), '.')]
        )

    def test_conditional_trigrams(self):
        trigrams = conditional_trigrams(nltk.trigrams(nltk.word_tokenize(self.TEST_CORPUS)))
        self.assertEqual(
            list(trigrams),
            [(('The', 'brown'), 'dog'), (('brown', 'dog'), 'jumped'), (('dog', 'jumped'), '.')]
        )

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

    def test_generate_sequence_terminates(self):
        generated = generate_sequence(self.cfd, ('c',), 3)
        expected = list('cd')
        self.assertEqual(generated, expected)

    def test_generate_sequence_assertion(self):
        with self.assertRaises(AssertionError):
            generate_sequence(self.cfd, ('c',), 4, condition_length=3)


class TestSentenceStarts(unittest.TestCase):
    """ Test that we are getting the starting sentences correctly. """
    SAMPLE_TEXT = "I am a test. This is another much longer test sentence."

    def setUp(self):
        sentences = nltk.tokenize.sent_tokenize(self.SAMPLE_TEXT)
        self.tokenized_sent = [nltk.tokenize.word_tokenize(sent) for sent in sentences]

    def test_sentence_starts(self):
        self.assertEqual(sentence_starts(self.tokenized_sent, 2), [("I", "am"), ("This", "is")])

    def test_sentence_starts_ignore_short_sentences(self):
        self.assertEqual(sentence_starts(self.tokenized_sent, 5), [("This", "is", "another", "much", "longer")])


class TestCharacterLimits(unittest.TestCase):
    """ Test to make sure

class TestTextCleaning(unittest.TestCase):
    """ Make sure we're cleaning text the way we expect."""

    def assertCleanedMatches(self, text_to_clean, expected):
        cleaned = clean_text(text_to_clean)
        self.assertEqual(cleaned, expected)

    def test_single_period(self):
        self.assertCleanedMatches("happy .", "happy.")

    def test_question_mark(self):
        self.assertCleanedMatches("happy ?", "happy?")

    def test_comma(self):
        self.assertCleanedMatches("happy ,", "happy,")

    def test_exclamation_point(self):
        self.assertCleanedMatches("happy !", "happy!")

    def test_apostrophe(self):
        self.assertCleanedMatches("he ' s", "he's")

    def test_quotation(self):
        self.assertCleanedMatches(' " Hello , " he ', ' "Hello," he ')
        self.assertCleanedMatches('" Hello , "', '"Hello,"')
