""" Generate a sequence of words. """

from __future__ import print_function
import re
import nltk
import random
import pickle

CORPUS_ROOT = 'corpus/'
PICKLE_FILE = 'model.pkl'
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
    # fix ending punctuation
    cleaned_text = re.sub(r'\s([?.!,;](?:\s|$))', r'\1', text)
    # fix apostrophes
    cleaned_text = re.sub(r" ([']) ", r"\1", cleaned_text)
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

    for _ in range(seq_length):
        next_word = get_random_choice(cfd[previous_tuple])
        if next_word is None:
            return sequence
        sequence.append(next_word)
        # get the last words in the list to use as the basis of the next search
        previous_tuple = tuple(sequence[-condition_length:])
    return sequence

def generate_model(file_root=CORPUS_ROOT, ngram_length=N, file_name=PICKLE_FILE):
    """
    Generate the model that gets used in the eventual text generation and pickles it out to a file.

    Args:
        file_root (str) - the path to the directory that we're using for our files
        ngram_length (int) - the length of the ngrams that we're using
        file_name (str) - the file name we want to use for the pickle file

    Returns:
        None

    """

    reader = nltk.corpus.PlaintextCorpusReader(file_root, '.*.txt')
    ngrams = nltk.ngrams(reader.words(), ngram_length)

    reader_cfd = nltk.ConditionalFreqDist(conditional_ngrams(ngrams, ngram_length))
    with open(file_name, 'wb') as pickle_file:
        pickle.dump(reader_cfd, pickle_file)
        

def generate_text_by_word_length(starting_seq, ngram_length=N, num_words=100, regen_model=False):
    """
    Generate text from the model using the given parameters.

    Args:
        starting_seq (tuple) - the tuple we would like to use to start the sequence.
        ngram_length (int) - the length of the ngrams that we would like to use to generate the text
        num_words (int) - the number of words in the text we'd like to generate
        regen_model (bool) - determines whether or not the model is regenerated before generating the text

    Returns:
        string containing the text that has been generated
    """

    assert len(starting_seq) == ngram_length - 1, "The starting sequence does not match the ngram length."

    if regen_model:
        generate_model(ngram_length=ngram_length)

    with open(PICKLE_FILE, 'rb') as pickle_file:
        reader_cfd = pickle.load(pickle_file)

    output_text = " ".join(generate_sequence(reader_cfd, starting_seq, num_words, condition_length=ngram_length-1))

    return clean_text(output_text)
