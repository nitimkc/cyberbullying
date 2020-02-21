# 1. read corpus
# 2. create loader object (iterable of train and test sets)

from reader import TweetsCorpusReader
from loader import CorpusLoader

import numpy as np
import nltk
import os
import json
import logging
import re

log = logging.getLogger("readability.readability")
log.setLevel('WARNING')

# #windows
# ROOT = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\'
# CORPUS = os.path.join(ROOT, 'data\\labelled_tweets\\b')
# RESULTS = os.path.join(ROOT, 'results')

#mac
ROOT = '/Users/peaceforlives/Documents/Projects/cyberbullying/'
CORPUS = os.path.join(ROOT, 'data/labelled_tweets')
RESULTS = os.path.join(ROOT, 'results')

DOC_PATTERN = r'.*\.json' 

target = 'bullying_trace'
if __name__ == '__main__':
    corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN, bullying_trace=target)
    loader = CorpusLoader(corpus, folds=12)
    print(loader.n_docs)
    print(loader.n_folds)
    print(loader.folds)
    print(loader.label)
    X = corpus.docs()
    y = corpus.labels
    for train_index, test_index in loader.folds.split(corpus.docs()):
        print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

    # docs   = loader.documents(0, test=True)
    # labels = loader.labels(0, test=True)
    # # print(next(docs)[0][0][0])
    # normal = TextNormalizer()
    # normal.fit(docs, labels)

    # docs   = list(normal.transform(docs))

    # vect = GensimVectorizer('lexicon.pkl')
    # vect.fit(docs)
    # docs = vect.transform(docs)
    # print(next(docs))