# 1. read corpus
# 2. create loader object (iterable of train and test sets)
# 3. run classification models in cv mode and
#    store cv scores in json file

from reader import TweetsCorpusReader
from loader import CorpusLoader
from build import binary_models
from build import multiclass_models
from build import score_models

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


##########################################################################
## binary-classification
##########################################################################


# target = 'bullying_trace'
# if __name__ == '__main__':
#     corpus = TweetsCorpusReader(CORPUS.__str__(), DOC_PATTERN, bullying_trace=target)
#     # perform classification with increasing training set size
#     idx = (np.linspace(1, 1.0, 1)*len(corpus.docs())).astype(int)
#     # idx = [i for i in range(0, len(corpus.docs()), 100) ]
#     for i in idx: 
#         loader = CorpusLoader(corpus, 12, label=target, size=i)
#         for scores in score_models(binary_models, loader):
#             result_filename = '/TRACE_results'+str(i)+'.json'
#             with open(RESULTS+result_filename, 'a') as f:
#                 f.write(json.dumps(scores) + "\n")



# ##########################################################################
# ## multi-classification
# ##########################################################################

# target = 'bullying_role'
# if __name__ == '__main__':
#     corpus = TweetsCorpusReader(CORPUS.__str__(), DOC_PATTERN, bullying_trace=target)
#     idx = (np.linspace(1, 1.0, 1)*len(corpus.docs())).astype(int)
#     # idx = [i for i in range(100, len(corpus.docs()), 100) ]
#     for i in idx: 
#         loader = CorpusLoader(corpus, 12, label=target, size=i)
#         for scores in score_models(multiclass_models, loader):
#             result_filename = '/ROLE_results'+str(i)+'.json'
#             with open(RESULTS+result_filename, 'a') as f:
#                 f.write(json.dumps(scores) + "\n")


# target = 'form_of_bullying'
# if __name__ == '__main__':
#     corpus = TweetsCorpusReader(CORPUS.__str__(), DOC_PATTERN, bullying_trace=target)
#     idx = (np.linspace(1, 1.0, 1)*len(corpus.docs())).astype(int)
#     # idx = [i for i in range(100, len(corpus.docs()), 100) ]
#     for i in idx: 
#         loader = CorpusLoader(corpus, 12, label=target, size=i)
#         for scores in score_models(multiclass_models, loader):
#             result_filename = '/FORM_results'+str(i)+'.json'
#             with open(RESULTS+result_filename, 'a') as f:
#                 f.write(json.dumps(scores) + "\n")


target = 'bullying_post_type'
if __name__ == '__main__':
    corpus = TweetsCorpusReader(CORPUS.__str__(), DOC_PATTERN, bullying_trace=target)
    # idx = (np.linspace(1, 1.0, 1)*len(corpus.docs())).astype(int)
    idx = [i for i in range(100, len(corpus.docs()), 100) ]
    for i in idx: 
        loader = CorpusLoader(corpus, 12, label=target, size=i)
        for scores in score_models(multiclass_models, loader):
            result_filename = '/TYPE_results'+str(i)+'.json'
            with open(RESULTS+result_filename, 'a') as f:
                f.write(json.dumps(scores) + "\n")