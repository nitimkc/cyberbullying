from reader import TweetsCorpusReader
from transformers import TextNormalizer, GensimVectorizer
from build_evaluate import build_and_evaluate   
from build_evaluate_svm  import build_and_evaluateSVM

from pathlib import Path
import numpy as np
import pandas as pd
import pickle
import nltk
import os
import json
import logging
import re

log = logging.getLogger("readability.readability")
log.setLevel('WARNING')

# ROOT = Path('C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\') # windows
ROOT = Path('/Users/peaceforlives/Documents/Projects/cyberbullying/')         # mac
CORPUS = Path.joinpath(ROOT, 'data', 'labelled_tweets', 'ab')
FULL_CORPUS = Path.joinpath(ROOT, 'data', 'located_tweets')
RESULTS = Path.joinpath(ROOT, 'results')

DOC_PATTERN = r'.*\.json'

#################################
# predictions for entire dataset
# 839680
#################################

# full_corpus = TweetsCorpusReader(FULL_CORPUS.__str__(), DOC_PATTERN, bullying_trace=None)
# docs = full_corpus.docs()
# print(len(docs))
# data_docs = pd.DataFrame(docs)
# print(data_docs.shape)
# data_docs.to_csv('results/full_data.csv', encoding='utf-8-sig')

# full_processedtweets = full_corpus.process_tweet()
# normalize  = TextNormalizer()
# full_X = list(normalize.fit_transform(full_processedtweets)) # X = [' '.join(doc) for doc in normalized_tweets]
# with open('results/full_X.txt', 'wb') as f:
#     pickle.dump(full_X, f)

# with open('results/full_X.txt', 'rb') as f:
#     full_X = pickle.load( f)
# print(len(full_X))

# labels = {'bullying_trace':['no','yes'],
#             'bullying_role':['accuser','bully','defender','other','reporter','victim'],
#             'form_of_bullying':['cyber','general','physical','verbal'],
#             'bullying_post_type':['accusation','cyberbullying','denial','report','self-disclosure']}
# targets = ['bullying_trace', 'bullying_role', 'form_of_bullying', 'bullying_post_type']
# for target in targets:
#     print(target)
#     PATH = 'results/'+target+".pickle"
#     with open(PATH, 'rb') as f:
#         model = pickle.load(f)
    
#     full_pred = model.predict(full_X)
#     from collections import Counter
#     Counter(full_pred)

#     label = {i:labels[target][i] for i in range(len(labels[target]))}
#     print(label)
#     data_docs[target] = list(map(label.get, full_pred))
#     if target!='bullying_trace':
#         data_docs.loc[data_docs['bullying_trace']=='no', target] = 'NA'
#     print(data_docs[target].value_counts())


# print(data_docs.columns)
# new_cols = ['id', 'full_tweet', 'bullying_trace', 'bullying_role', 'form_of_bullying', 'bullying_post_type']
# data_docs = data_docs[new_cols]
# data_docs.to_pickle("data_docs.pkl")


################################################################################
# 2500 sample of bullying and non bullying trace tweets as predicted by machine
################################################################################

# yes = data_docs[data_docs['bullying_trace']=='yes']
# yes_sample = yes.sample(n=2500)

# no = data_docs.loc[data_docs['bullying_trace']=='no']
# no_sample = no.sample(n=2500)

# sample_tweets = pd.concat([yes_sample,no_sample])
# sample_tweets = sample_tweets.sample(frac=1)
# sample_tweets.to_csv('results/sample_tweets.csv', encoding='utf-8-sig', index=False)


#####################
# read saved files
####################
sample_tweets = pd.read_csv('results/sample_tweets.csv', encoding='utf-8-sig')
data_docs = pd.read_pickle("results/data_docs.pkl")
