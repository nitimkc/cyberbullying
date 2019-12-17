# 1. read corpus
# 2. create loader object (iterable of train and test sets)
# 3. run classification models in cv model and
#    store cv scores in json file

from reader import TweetsCorpusReader
from loader import CorpusLoader
from build import models
from build import score_models

import nltk
import os
import json
import logging
import re

log = logging.getLogger("readability.readability")
log.setLevel('WARNING')

ROOT = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\'
CORPUS = os.path.join(ROOT, 'data\\labelled_tweets')
RESULTS = os.path.join(ROOT, 'results')

DOC_PATTERN = r'.*\.json' 

# file = CORPUS+'\\random_tweets_2b.json'


if __name__ == '__main__':
    corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN)
    loader = CorpusLoader(corpus, 12, label='bullying_trace')
    for scores in score_models(models, loader):
        with open(RESULTS+'\\results.json', 'a') as f:
            f.write(json.dumps(scores) + "\n")
