import nltk

root = 'corpus/'

reader = nltk.corpus.PlaintextCorpusReader(root, '.*.txt')
#sentences = reader.sents()

text = nltk.Text(reader.words())
text.generate()
