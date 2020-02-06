# 1. read corpus
# 2. create loader object (iterable of train and test sets)
# 3. run classification models in cv mode and
#    store cv scores in json file

from reader import TweetsCorpusReader
from loader import CorpusLoader
from build import binary_models
from build import multiclass_models
from build import score_models

import numpy as np
import nltk
import os
import json
import logging
import re

log = logging.getLogger("readability.readability")
log.setLevel('WARNING')

#windows
ROOT = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\'
CORPUS = os.path.join(ROOT, 'data\\labelled_tweets\\ab')
RESULTS = os.path.join(ROOT, 'results')

#mac
# ROOT = '/Users/peaceforlives/Documents/Projects/cyberbullying/'
# CORPUS = os.path.join(ROOT, 'data/labelled_tweets')
# RESULTS = os.path.join(ROOT, 'results')

DOC_PATTERN = r'.*\.json' 


##########################################################################
## binary-classification
##########################################################################

# target = 'bullying_trace'
# result_filename = '/TRACE_results.json'
# if __name__ == '__main__':
#     corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN, bullying_trace=target)
#     loader = CorpusLoader(corpus, 5, label=target)
#     # idx = (np.linspace(.1, 1.0, 10)*len(corpus.docs())).astype(int)
#     for scores in score_models(binary_models, loader):
#         with open(RESULTS+result_filename, 'a') as f:
#             f.write(json.dumps(scores) + "\n")


target = 'bullying_trace'
if __name__ == '__main__':
    corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN, bullying_trace=target)
    # perform classification with increasing training set size
    idx = (np.linspace(1, 1.0, 1)*len(corpus.docs())).astype(int)
    for i in idx: 
        loader = CorpusLoader(corpus, 12, label=target, size=i)
        for scores in score_models(binary_models, loader):
            result_filename = '/TRACE_results'+str(i)+'.json'
            with open(RESULTS+result_filename, 'a') as f:
                f.write(json.dumps(scores) + "\n")



# ##########################################################################
# ## multi-classification
# ##########################################################################

# target = 'bullying_role'
# result_filename = '/ROLE_results.json'
# if __name__ == '__main__':
#     corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN, bullying_trace=target)
#     loader = CorpusLoader(corpus, 5, label=target)
#     for scores in score_models(multiclass_models, loader):
#         with open(RESULTS+result_filename, 'a') as f:
#             f.write(json.dumps(scores) + "\n")

# target = 'form_of_bullying'
# result_filename = '/FORM_results.json'
# if __name__ == '__main__':
#     corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN, bullying_trace=target)
#     loader = CorpusLoader(corpus, 5, label=target)
#     for scores in score_models(multiclass_models, loader):
#         with open(RESULTS+result_filename, 'a') as f:
#             f.write(json.dumps(scores) + "\n")


# target = 'bullying_post_type'
# result_filename = '/TYPE_results.json'
# if __name__ == '__main__':
#     corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN, bullying_trace=target)
#     loader = CorpusLoader(corpus, 5, label=target)
#     for scores in score_models(multiclass_models, loader):
#         with open(RESULTS+result_filename, 'a') as f:
#             f.write(json.dumps(scores) + "\n")