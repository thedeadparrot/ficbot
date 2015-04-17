"""
This is the script you would run in order to generate text directly from the command line.

Usage:
    python generation_script.py "Hello world"

"""
from __future__ import print_function

import argparse
import nltk

from generator import generate_text

parser = argparse.ArgumentParser(description='Generate text using simple ngram models')

parser.add_argument(
    '--regen', '-r', action='store_true', dest='regen_model', default=False, help='Force a regeneration of the model'
)
parser.add_argument('--ngram-length', '-n', action='store', dest='ngram_length', type=int, default=3, help='The number of elements in the n-grams we will be using. Default: 3')
parser.add_argument('--words', '-w', action='store', dest='num_words', type=int, default=100, help="The number of words to generate. Default: 100")
parser.add_argument('starting_text', action='store', help="The text we will use to start the text generation.")

args = parser.parse_args()

# tuple-ize the starting text that gets passed in
starting_text = tuple(nltk.word_tokenize(args.starting_text))


# run the generator with the given options
try:
    print(generate_text(starting_text, ngram_length=args.ngram_length, num_words=args.num_words, regen_model=args.regen_model))
except AssertionError as assertion:
    print("ERROR:")
    print("\t{}".format(assertion.message))
    print("\tYou may need to regenerate the model first. Run the command again with the -r flag.")
