""" Generate a sequence of words. """

from __future__ import print_function
import re
import nltk
import random
import pickle

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
    rand = random.randint(0, total_samples)
    running_tot = 0
    # iterate over all the possible bins
    for index in range(1, word_dist.B() + 1):
        # add the number of incidences of the current word to the total
        running_tot += word_dist.most_common(index)[-1][1]
        # if the random number falls into the current bucket, return this word
        if rand <= running_tot:
            return word_dist.most_common(index)[-1][0]


def clean_text(text):
    """ Clean up common oddnesses, like spaces before punctuation and such. """
    # fix ending punctuation
    cleaned_text = re.sub(r'\s([?.!,](?:\s|$))', r'\1', text)
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
    # when
    assert len(previous_tuple) == condition_length, "Tuple passed in is not the right length."
    sequence = list(previous_tuple)

    for _ in range(seq_length):
        next_word = get_random_choice(cfd[previous_tuple])
        sequence.append(next_word)
        # get the last words in the list to use as the basis of the next search
        previous_tuple = tuple(sequence[-condition_length:])
        if next_word is None:
            return sequence
    return sequence

def generate_model(file_root='corpus/'):

    reader = nltk.corpus.PlaintextCorpusReader(file_root, '.*.txt')
    ngrams = nltk.ngrams(reader.words(), N)

    reader_cfd = nltk.ConditionalFreqDist(conditional_ngrams(ngrams, N))
    with open(PICKLE_FILE, 'w') as pickle_file:
        pickle.dump(reader_cfd, pickle_file)
        

def generate_text(starting_seq, character_length=140, regen_model=False):

    if regen_model:
        generate_model()

    with open(PICKLE_FILE, 'r') as pickle_file:
        reader_cfd = pickle.load(pickle_file)

    output_text = " ".join(generate_sequence(reader_cfd, starting_seq, 200, condition_length=N-1))

    print(clean_text(output_text))
