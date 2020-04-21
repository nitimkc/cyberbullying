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


# if __name__ == "__main__":

labels = {'bullying_trace':['no','yes'],
            'bullying_role':['accuser','bully','defender','other','reporter','victim'],
            'form_of_bullying':['cyber','general','physical','verbal'],
            'bullying_post_type':['accusation','cyberbullying','denial','report','self-disclosure']}


target = 'bullying_trace'
#############################
PATH = 'results/'+target+".pickle"
label = {i:categories[i] for i in range(len(labels[target]))}

# if not os.path.exists(PATH):
corpus = TweetsCorpusReader(CORPUS.__str__(), DOC_PATTERN, bullying_trace=target)     
processed_tweets = corpus.process_tweet()
normalize = TextNormalizer()
X = list(normalize.fit_transform(processed_tweets)) 
y = list(corpus.fields(target))
model, y_pred, idx_test = build_and_evaluate(X, y, outpath=PATH, n=0.2) # get the index of test set
# y_pred_new = model.predict(X[i] for i in idx_test)
# from build_evaluate import show_most_informative_features
# print(show_most_informative_features(model))

target_data = pd.DataFrame(corpus.docs())
target_data = target_data[['full_tweet', target]]
test_data = target_data.iloc[idx_test,]
test_data['pred'] = list(map(label.get, y_pred))
test_data.to_csv('results/'+target+'.csv', encoding='utf-8') # save test set with actual and predicted labels


target = 'bullying_role'
#############################
PATH = 'results/'+target+".pickle"
label = {i:categories[i] for i in range(len(labels[target]))}

# if not os.path.exists(PATH):
corpus = TweetsCorpusReader(CORPUS.__str__(), DOC_PATTERN, bullying_trace=target)     
processed_tweets = corpus.process_tweet()
normalize = TextNormalizer()
X = list(normalize.fit_transform(processed_tweets)) 
y = list(corpus.fields(target))
model, y_pred, idx_test = build_and_evaluateSVM(X, y, outpath=PATH, n=0.2) # get the index of test set
# y_pred_new = model.predict(X[i] for i in idx_test)

target_data = pd.DataFrame(corpus.docs())
target_data = target_data[['full_tweet', target]]
test_data = target_data.iloc[idx_test,]
test_data['pred'] = list(map(label.get, y_pred))
test_data.to_csv('results/'+target+'.csv', encoding='utf-8') # save test set with actual and predicted labels


target = 'form_of_bullying'
#############################
PATH = 'results/'+target+".pickle"
label = {i:categories[i] for i in range(len(labels[target]))}

# if not os.path.exists(PATH):
corpus = TweetsCorpusReader(CORPUS.__str__(), DOC_PATTERN, bullying_trace=target)     
processed_tweets = corpus.process_tweet()
normalize = TextNormalizer()
X = list(normalize.fit_transform(processed_tweets)) 
y = list(corpus.fields(target))
model, y_pred, idx_test = build_and_evaluateSVM(X, y, outpath=PATH, n=0.2) # get the index of test set
# y_pred_new = model.predict(X[i] for i in idx_test)

target_data = pd.DataFrame(corpus.docs())
target_data = target_data[['full_tweet', target]]
test_data = target_data.iloc[idx_test,]
test_data['pred'] = list(map(label.get, y_pred))
test_data.to_csv('results/'+target+'.csv', encoding='utf-8') # save test set with actual and predicted labels


target = 'bullying_post_type'
#############################
PATH = 'results/'+target+".pickle"
label = {i:categories[i] for i in range(len(labels[target]))}

# if not os.path.exists(PATH):
corpus = TweetsCorpusReader(CORPUS.__str__(), DOC_PATTERN, bullying_trace=target)     
processed_tweets = corpus.process_tweet()
normalize = TextNormalizer()
X = list(normalize.fit_transform(processed_tweets)) 
y = list(corpus.fields(target))
model, y_pred, idx_test = build_and_evaluate(X, y, outpath=PATH, n=0.2, multiclass=True) # get the index of test set
# y_pred_new = model.predict(X[i] for i in idx_test)
# from build_evaluate import show_most_informative_features
# print(show_most_informative_features(model))

target_data = pd.DataFrame(corpus.docs())
target_data = target_data[['full_tweet', target]]
test_data = target_data.iloc[idx_test,]
test_data['pred'] = list(map(label.get, y_pred))
test_data.to_csv('results/'+target+'.csv', encoding='utf-8') # save test set with actual and predicted labels


