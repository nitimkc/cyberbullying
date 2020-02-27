# 1. read corpus
# 2. create loader object (iterable of train and test sets)

from reader import TweetsCorpusReader
from loader import CorpusLoader
from transformers import TextNormalizer_lemmatize, GensimVectorizer
from sklearn.preprocessing import LabelEncoder

from pathlib import Path
import numpy as np
import nltk
import os
import json
import logging
import re

log = logging.getLogger("readability.readability")
log.setLevel('WARNING')


ROOT = Path('C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\') # windows
# ROOT = Path('/Users/peaceforlives/Documents/Projects/cyberbullying/')         # mac
CORPUS = Path.joinpath(ROOT, 'data', 'labelled_tweets', 'b')
RESULTS = Path.joinpath(ROOT, 'results')

DOC_PATTERN = r'.*\.json' 

target = 'bullying_trace'
if __name__ == '__main__':

    from sklearn.pipeline import Pipeline
    from sklearn.linear_model import LogisticRegression
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.metrics import accuracy_score

    corpus = TweetsCorpusReader(CORPUS.__str__(), DOC_PATTERN, bullying_trace=target)
    docs = corpus.process_tweet()
    labels = list(corpus.fields(target))

   