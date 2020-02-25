# 1. read corpus
# 2. create loader object (iterable of train and test sets)

from reader import TweetsCorpusReader
from loader import CorpusLoader
from transformers import TextNormalizer_lemmatize

from pathlib import Path
import numpy as np
import nltk
import os
import json
import logging
import re

log = logging.getLogger("readability.readability")
log.setLevel('WARNING')


# ROOT = Path('C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\') # windows
ROOT = Path('/Users/peaceforlives/Documents/Projects/cyberbullying/')         # mac
CORPUS = Path.joinpath(ROOT, 'data', 'labelled_tweets', 'b')
RESULTS = Path.joinpath(ROOT, 'results')

DOC_PATTERN = r'.*\.json' 

target = 'bullying_trace'
if __name__ == '__main__':
    corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN, bullying_trace=target)
    docs = corpus.process_tweet()
    labels = list(corpus.fields(target))
    normal = TextNormalizer_lemmatize()
    normal.fit(docs, labels)
    docs   = list(normal.transform(docs))
    # import gensim
    # from gensim.matutils import sparse2full
    # id2word = gensim.corpora.Dictionary()
    # for doc in docs:
    #     for tweet in doc:
    #         print(tweet)

    #         docvec = id2word.doc2bow(tweet)

    from transformers import GensimVectorizer
    vect = GensimVectorizer('lexicon.pkl')
    vect.fit(docs)
    docs = vect.transform(docs)
    print(next(docs))

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