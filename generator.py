""" Generate a sequence of words. """

from __future__ import print_function
import re
import random
import cPickle as pickle
import json

import nltk

CORPUS_ROOT = 'corpus/'
MODEL_FILE = 'model.pkl'
SENTENCE_FILE = 'sents.json'
N = 3


def conditional_bigrams(bigram_list):
    """ Generates a set of bigrams that look like (tuple, word) for the sake of consistency.
    """
    for bigram in bigram_list:
        yield ((bigram[0],), bigram[1])


def conditional_trigrams(trigram_list):
    """ Generates a set of trigrams that look like (tuple, word) for the sake of consistency.
    """
    for trigram in trigram_list:
        yield ((trigram[0], trigram[1]), trigram[2])


def conditional_ngrams(ngram_list, n):
    for ngram in ngram_list:
        yield (tuple(ngram[:(n - 1)]), ngram[-1])


def get_random_choice(word_dist):
    """
    Given a word distribution, pick one at random based on how common
    it is.

    Args:
        word_dist (FreqDist) - a frequency distribution of words
    Returns:
        string - a random word from word_dist
    """
    total_samples = word_dist.N()
    random_sample = random.randint(0, total_samples)
    running_total = 0
    # iterate over all the possible bins
    for word_bin in word_dist.most_common(word_dist.B()):
        # add the number of incidences of the current word to the total
        running_total += word_bin[1]
        # if the random number falls into the current bucket, return this word
        if random_sample <= running_total:
            return word_bin[0]


def clean_text(text):
    """ Clean up common oddnesses, like spaces before punctuation and such. """
    # fix quotation marks
    # ugh, special case the start of a string
    starting = False if re.search('^" ', text) else True
    cleaned_text = re.sub(r'^" ', '"', text)
    while re.search(r' " ', cleaned_text):
        # add a space before the quotation mark
        if starting:
            cleaned_text = re.sub(' " ', ' "', cleaned_text, count=1)
        # add a space after the quotation mark
        else:
            cleaned_text = re.sub(' " ', '" ', cleaned_text, count=1)
        # alternate between starting and not starting
        starting = not starting

    # aaaaaan special case ending
    if not starting:
        cleaned_text = re.sub(r' "$', '"', cleaned_text)

    # fix apostrophes
    cleaned_text = re.sub(r"\s(['])\s", r"\1", cleaned_text)

    # fix ending punctuation
    cleaned_text = re.sub(r'\s([\?.!,;])', r'\1', cleaned_text)
    return cleaned_text


def generate_sequence(cfd, previous_tuple, seq_length=10, condition_length=1):
    """
    Generate a sequence of words based on a ConditionalFreqDist.

    Args:
        cfd - A ConditionalFreqDist
        previous_tuple (tuple) - the starting condition that will lead the sequence
        seq_length (int)- the number of words to generate for the sequence
        condition_length (int) - the length of previous_tuple and the number of elements in the starting condition

    Returns:
        a list of words
    """
    # when the previous_tuple that gets passed in is not the correct length, assert an error
    assert len(previous_tuple) == condition_length, "Starting tuple is not the right length."
    sequence = list(previous_tuple)

    for _ in range(seq_length - condition_length):
        next_word = get_random_choice(cfd[previous_tuple])
        if next_word is None:
            return sequence
        sequence.append(next_word)
        # get the last words in the list to use as the basis of the next search
        previous_tuple = tuple(sequence[-condition_length:])
    return sequence


def sentence_starts(sentences, start_length):
    """
    Returns a list of tuples that contain the first start_length number of words from a list of sentences.
    """
    # pull all the sentence starts
    starts = []
    for sentence in sentences:
        if len(sentence) > start_length:
            starts.append(tuple(sentence[:start_length]))
    return starts


def enforce_character_limit(sequence, character_limit):
    """
    Truncate the sequence such that the words inside it fit inside the character limit.

    Args:
        - sequence (list of str) - The sequence of words that need to be truncated
        - character_limit (int) - the number of characters that can be in our final text sequence

    Returns:
        A list of str, where the number of characters in the strings (plus spaces) fit inside character_limit.
    """
    final_sequence = []
    character_length = 0
    for word in sequence:
        # Add the length of the word plus one space.
        # This overestimates the length, but that's fine.
        character_length = character_length + len(word) + 1
        if character_length > character_limit:
            break
        final_sequence.append(word)

    return final_sequence


def generate_model(file_root=CORPUS_ROOT, ngram_length=N, model_file=MODEL_FILE, sentence_file=SENTENCE_FILE):
    """
    Generate the model that gets used in the eventual text generation and pickles it out to a file.

    Also save the starts of sentences such that they can be used to seed the text generation.

    Args:
        file_root (str) - the path to the directory that we're using for our files
        ngram_length (int) - the length of the ngrams that we're using
        file_name (str) - the file name we want to use for the pickle file

    Returns:
        None

    """

    reader = nltk.corpus.PlaintextCorpusReader(file_root, '.*.txt')
    ngrams = nltk.ngrams(reader.words(), ngram_length)

    starts = sentence_starts(reader.sents(), ngram_length-1)

    reader_cfd = nltk.ConditionalFreqDist(conditional_ngrams(ngrams, ngram_length))

    with open(model_file, 'wb') as m_file:
        pickle.dump(reader_cfd, m_file)

    with open(sentence_file, 'wb') as sent_file:
        json.dump(starts, sent_file)


def generate_text(starting_seq=None,
                  ngram_length=N,
                  num_words=100,
                  limit_characters=None,
                  reader_cfd=None,
                  model_file=MODEL_FILE,
                  sentence_file=SENTENCE_FILE):
    """
    Generate text from the model using the given parameters.

    Args:
        starting_seq (tuple) - the tuple we would like to use to start the sequence.
        ngram_length (int) - the length of the ngrams that we would like to use to generate the text
        num_words (int) - the number of words in the text we'd like to generate
        regen_model (bool) - determines whether or not the model is regenerated before generating the text
        limit_characters (int or None) - if this value has been set, truncate the output so that
                                         it is shorter than the given number of characters
        reader_cfd (ConditionalFreqDist) - The CFD to use in our generation. Mostly used because unpickling is slow.
    Returns:
        string containing the text that has been generated
    """

    # we can only check this if we have been given a starting sequence
    if starting_seq:
        assert len(starting_seq) == ngram_length - 1, "The starting sequence does not match the ngram length."

    if not reader_cfd:
        with open(model_file, 'rb') as m_file:
            reader_cfd = pickle.load(m_file)

    # if we don't have a starting sequence, pick one at random from our list
    if not starting_seq:
        with open(sentence_file, 'rb') as sent_file:
            starts = [tuple(start) for start in json.load(sent_file)]
            starting_seq = random.choice(starts)

    sequence = generate_sequence(
        reader_cfd, starting_seq, num_words, condition_length=ngram_length-1
    )

    if limit_characters:
        sequence = enforce_character_limit(sequence, limit_characters)

    output_text = " ".join(sequence)

    return clean_text(output_text)
