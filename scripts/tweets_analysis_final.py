from reader import TweetsCorpusReader
from loader import CorpusLoader

from sklearn.model_selection import train_test_split as tts
from build import models
from build import score_models

from sklearn.pipeline import Pipeline

import nltk
import os
import json
import pickle
import logging
import re

log = logging.getLogger("readability.readability")
log.setLevel('WARNING')

ROOT = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\'
CORPUS = os.path.join(ROOT, 'data\\labelled_tweets')
RESULTS = os.path.join(ROOT, 'results')
DOC_PATTERN = r'.*\.json' 
file = CORPUS+'\\random_tweets_2b.json'

# PICKLED = os.path.join(ROOT, 'data\\pickled\\labelled_tweets')
# PKL_PATTERN = r'.*\.pickle'
# file = PICKLED+'\\random_tweets_2b.pickle'


if __name__ == '__main__':
    corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN)
    # print(reader.describes())  
    # docs = corpus.process_tweet()
    # bullying_trace = list(corpus.fields('bullying_trace'))

    # pkl = Preprocessor(corpus, PICKLED)
    # processed_tokens = pkl.transform()
    # pkl_corpus = PickledCorpusReader(PICKLED)
    

    loader = CorpusLoader(corpus, 12, label='bullying_trace')
    for scores in score_models(models, loader):
        with open(RESULTS+'\\results.json', 'a') as f:
            f.write(json.dumps(scores) + "\n")
