""" Generate a sequence of words. """

from __future__ import print_function
import nltk
import random


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
    #print('rand: {}, total samples: {}, number_bins: {}'.format(rand, total_samples, word_dist.B()))
    # iterate over all the possible bins
    for index in range(1, word_dist.B() + 1):
        # add the number of incidences of the current word to the total
        running_tot += word_dist.most_common(index)[-1][1]
        # if the random number falls into the current bucket, return this word
        if rand <= running_tot:
            return word_dist.most_common(index)[-1][0]


def generate_sequence(cfd, word, num=10):
    """
    Generate a sequence of words based on a ConditionalFreqDist.

    Args:
        cfd - A ConditionalFreqDist
        word - the word that will start the sequence
        num - the number of words to generate for the sequence

    Returns:
        a list of words
    """
    sequence = []
    for _ in range(num):
        sequence.append(word)
        word = get_random_choice(cfd[word])
        if word is None:
            word = get_random_choice(random.choice(cfd))
    return sequence


root = 'corpus/'

reader = nltk.corpus.PlaintextCorpusReader(root, '.*.txt')
bigrams = nltk.bigrams(reader.words())

reader_cfd = nltk.ConditionalFreqDist(bigrams)

print(" ".join(generate_sequence(reader_cfd, 'Blaine', 400)))
