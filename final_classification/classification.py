# 1. read corpus
# 2. create loader object (iterable of train and test sets)
# 3. 

from reader import TweetsCorpusReader
from transformers import TextNormalizer_lemmatize, GensimVectorizer
from build_evaluate import build_and_evaluate   
from build_evaluate_svm  import build_and_evaluateSVM

from pathlib import Path
import numpy as np
import pickle
import nltk
import os
import json
import logging
import re

log = logging.getLogger("readability.readability")
log.setLevel('WARNING')

ROOT = Path('C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\') # windows
# ROOT = Path('/Users/peaceforlives/Documents/Projects/cyberbullying/')         # mac
CORPUS = Path.joinpath(ROOT, 'data', 'labelled_tweets', 'ab')
CORPUS_PRED = Path.joinpath(ROOT, 'data', 'filtered')
RESULTS = Path.joinpath(ROOT, 'results')

DOC_PATTERN = r'.*\.json'   
# file = CORPUS+'/tweets.json'


if __name__ == "__main__":

    corpus_pred = TweetsCorpusReader(CORPUS_PRED.__str__(), DOC_PATTERN, bullying_trace=None)
    docs = corpus_pred.docs()
    processed_predtweets = corpus_pred.process_tweet()

    normalize  = TextNormalizer_lemmatize()
    X_pred = list(normalize.fit_transform(processed_predtweets)) # X = [' '.join(doc) for doc in normalized_tweets]
    
    target = 'bullying_trace'
    #############################
    PATH = target+".pickle"
    # if not os.path.exists(PATH):
    # Time to build the model
    corpus = TweetsCorpusReader(CORPUS.__str__(), DOC_PATTERN, bullying_trace=target)        
    processed_tweets = corpus.process_tweet()
    normalize  = TextNormalizer_lemmatize()
    X = list(normalize.fit_transform(processed_tweets)) # X = [' '.join(doc) for doc in normalized_tweets]
    y = list(corpus.fields(target))
    model = build_and_evaluate(X, y, outpath=PATH, n=0.2)
    # else:
    #     with open(PATH, 'rb') as f:
    #         model = pickle.load(f)
    from build_evaluate import show_most_informative_features
    print(show_most_informative_features(model))

    y_pred = model.predict(X_pred)
    labels = {0:'no', 1:'yes'}
    y_pred = list(map(labels.get, y_pred))
    for (tweet,pred) in zip(docs, y_pred):
        tweet.update({target:pred})


    target = 'bullying_role'
    #############################
    PATH = target+".pickle"
    # if not os.path.exists(PATH):
    # Time to build the model
    corpus = TweetsCorpusReader(CORPUS.__str__(), DOC_PATTERN, bullying_trace=target)        
    processed_tweets = corpus.process_tweet()
    normalize  = TextNormalizer_lemmatize()
    X = list(normalize.fit_transform(processed_tweets)) # X = [' '.join(doc) for doc in normalized_tweets]
    y = list(corpus.fields(target))
    y = ['other' if i=='bystander' or i=='reinforcer' or i=='assistant'  else i for i in y]
    model = build_and_evaluateSVM(X, y, outpath=PATH, n=0.2)
    # else:
    #     with open(PATH, 'rb') as f:
    #         model = pickle.load(f)

    y_pred = model.predict(X_pred)
    labels = {0:'accuser', 1:'bully', 2:'defender', 3:'other', 4:'reporter', 5:'victim'}
    y_pred = list(map(labels.get, y_pred))
    for (tweet,pred) in zip(docs, y_pred):
        tweet.update({target:pred})


    target = 'form_of_bullying'
    #############################
    PATH = target+".pickle"
    # if not os.path.exists(PATH):
    # Time to build the model
    corpus = TweetsCorpusReader(CORPUS.__str__(), DOC_PATTERN, bullying_trace=target)        
    processed_tweets = corpus.process_tweet()
    normalize  = TextNormalizer_lemmatize()
    X = list(normalize.fit_transform(processed_tweets)) # X = [' '.join(doc) for doc in normalized_tweets]
    y = list(corpus.fields(target))
    model = build_and_evaluateSVM(X, y, outpath=PATH, n=0.2)
    # else:
    #     with open(PATH, 'rb') as f:
    #         model = pickle.load(f)
    from build_evaluate import show_most_informative_features
    print(show_most_informative_features(model))

    y_pred = model.predict(X_pred)
    labels = {0:'cyber', 1:'general', 2:'physical', 3:'verbal'}
    y_pred = list(map(labels.get, y_pred))
    for (tweet,pred) in zip(docs, y_pred):
        tweet.update({target:pred})


    target = 'bullying_post_type'
    PATH = target+".pickle"
    # if not os.path.exists(PATH):
    # Time to build the model
    corpus = TweetsCorpusReader(CORPUS.__str__(), DOC_PATTERN, bullying_trace=target)        
    processed_tweets = corpus.process_tweet()
    normalize  = TextNormalizer_lemmatize()
    X = list(normalize.fit_transform(processed_tweets)) # X = [' '.join(doc) for doc in normalized_tweets]
    y = list(corpus.fields(target))
    model = build_and_evaluate(X, y, outpath=PATH, n=0.2, multiclass=True)  
    # else:
    #     with open(PATH, 'rb') as f:
    #         model = pickle.load(f)
    from build_evaluate import show_most_informative_features
    print(show_most_informative_features(model))

    y_pred = model.predict(X_pred)
    labels = {0:'accusation', 1:'cyberbullying', 2:'denial', 3:'report', 4:'self-disclosure'}
    y_pred = list(map(labels.get, y_pred))
    for (tweet,pred) in zip(docs, y_pred):
        tweet.update({target:pred})

