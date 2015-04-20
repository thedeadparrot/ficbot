""" Tests for generating the model. """

import unittest
import random
import os
import json

import ddt
import nltk
import six
import cPickle as pickle

from generator import (conditional_ngrams, conditional_bigrams, conditional_trigrams,
                       get_random_choice, generate_sequence, clean_text, sentence_starts, enforce_character_limit,
                       generate_model, generate_text)


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
        # generate a dist with a different ngram length
        self.cfd3 = nltk.ConditionalFreqDist(conditional_ngrams(nltk.ngrams(self.TEST_CORPUS, 3), 3))

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

    def test_get_random_word_trigram(self):
        word = get_random_choice(self.cfd3[('b', 'b')])
        self.assertEqual(word, 'a')



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
    """ Test to make sure the character limits are what we expect. """
    SAMPLE_SEQUENCE = ["I", "am", "a", "sequence", "."]

    def test_enforce_limits_general(self):
        enforced = enforce_character_limit(self.SAMPLE_SEQUENCE, 5)
        self.assertEqual(enforced, ["I", "am"])

    def test_enforce_limits_borderline(self):
        enforced = enforce_character_limit(self.SAMPLE_SEQUENCE, 4)
        self.assertEqual(enforced, ["I"])

    def test_enforce_limits_generous(self):
        enforced = enforce_character_limit(self.SAMPLE_SEQUENCE, 200)
        self.assertEqual(enforced, self.SAMPLE_SEQUENCE)


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


class TestModelGeneration(unittest.TestCase):
    """ Test generating the model files. """
    TEST_MODEL_FILE = 'tests/test_model.pkl'
    TEST_SENTENCES_FILE = 'tests/test_sents_file.json'
    TEST_CORPUS = 'tests/test_corpus/'

    def setUp(self):
        generate_model(
            file_root=self.TEST_CORPUS, model_file=self.TEST_MODEL_FILE, sentence_file=self.TEST_SENTENCES_FILE
        )

    def test_model_generation_cfd(self):
        # load the file back in again
        with open(self.TEST_MODEL_FILE, 'rb') as m_file:
            cfd = pickle.load(m_file)

        self.assertIn(('Hello', ','), set(cfd.keys()))
        self.assertIn(('this', 'is'), set(cfd.keys()))

    def test_model_generation_sent(self):
        with open(self.TEST_SENTENCES_FILE, 'rb') as sent_file:
            sentence_starts = json.load(sent_file)

        self.assertEqual([['Hello', ',']], sentence_starts)

    def tearDown(self):
        os.remove(self.TEST_MODEL_FILE)
        os.remove(self.TEST_SENTENCES_FILE)


@ddt.ddt
class TestGenerateText(TestModelGeneration):
    """ Test to make sure text generation and associated options are working as expected. """

    def setUp(self):
        super(TestGenerateText, self).setUp()
        random.seed(1)

    def generate_text_pre_loaded(self, **kwargs):
        """ We are always going to be using these test files, so we might as well abstract them away. """
        return generate_text(model_file=self.TEST_MODEL_FILE, sentence_file=self.TEST_SENTENCES_FILE, **kwargs)

    def test_text_generation_simple(self):
        text = self.generate_text_pre_loaded(num_words=3)
        self.assertEqual("Hello, and this is", text)

    def test_text_generation_limit_characters(self):
        limit = 6
        text = self.generate_text_pre_loaded(num_words=5, limit_characters=limit)
        self.assertTrue(len(text) < limit)

    def test_text_generation_with_starting_sequence(self):
        text = self.generate_text_pre_loaded(num_words=3, starting_seq=("is", "a"))
        self.assertEqual("is a test file.", text)

    @ddt.data((2, "Hello,"), (4, "Hello, and this"))
    @ddt.unpack
    def test_ngram_length(self, ngram_length, expected_value):
        generate_model(
            file_root=self.TEST_CORPUS, model_file=self.TEST_MODEL_FILE, sentence_file=self.TEST_SENTENCES_FILE,
            ngram_length=ngram_length
        )
        text = self.generate_text_pre_loaded(num_words=1, ngram_length=ngram_length)
        self.assertEqual(text, expected_value)
