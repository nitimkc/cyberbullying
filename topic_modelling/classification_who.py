# 1. read corpus
# 2. create loader object (iterable of train and test sets)
# 3. run classification models in cv mode and
#    store cv scores in json file

from reader_who import TweetsCorpusReader
from loader import CorpusLoader
from build_multiclassification import models
from build_multiclassification import score_models

import nltk
import os
import json
import logging
import re

log = logging.getLogger("readability.readability")
log.setLevel('WARNING')

ROOT = '/Users/peaceforlives/Documents/Projects/cyberbullying/'
CORPUS = os.path.join(ROOT, 'data/labelled_tweets')
RESULTS = os.path.join(ROOT, 'results')

DOC_PATTERN = r'.*\.json' 

result_filename = '/ROLE_results.json'
target = 'bullying_role'

if __name__ == '__main__':
    corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN, bullying_trace=target)
    loader = CorpusLoader(corpus, 12, label=target)
    for scores in score_models(models, loader):
        with open(RESULTS+result_filename, 'a') as f:
            f.write(json.dumps(scores) + "\n")


result_filename = '/FORM_results.json'
target = 'form_of_bullying'

if __name__ == '__main__':
    corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN, bullying_trace=target)
    loader = CorpusLoader(corpus, 12, label=target)
    for scores in score_models(models, loader):
        with open(RESULTS+result_filename, 'a') as f:
            f.write(json.dumps(scores) + "\n")

result_filename = '/TYPE_results.json'
target = 'bullying_post_type'

if __name__ == '__main__':
    corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN, bullying_trace=target)
    loader = CorpusLoader(corpus, 12, label=target)
    for scores in score_models(models, loader):
        with open(RESULTS+result_filename, 'a') as f:
            f.write(json.dumps(scores) + "\n")