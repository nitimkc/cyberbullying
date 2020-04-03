# 1. read corpus
# 2. create loader object (iterable of train and test sets)
# 3. 

from reader import TweetsCorpusReader
from transformers import TextNormalizer_lemmatize, GensimVectorizer
from pathlib import Path
import numpy as np
import pickle
import nltk
import os
import json
import logging
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import classification_report as clsr
from sklearn.metrics import confusion_matrix as cm
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


log = logging.getLogger("readability.readability")
log.setLevel('WARNING')

def identity(words):
    return words

def train_model(classifier, feature_vector_train, label, feature_vector_valid, valid_y, is_neural_net=False):
    
    classifier.fit(feature_vector_train, label)
    predictions = classifier.predict(feature_vector_valid)
    
    if is_neural_net:
        predictions = predictions.argmax(axis=-1)
    
    return accuracy_score(predictions, valid_y)


data = 'ab'
ROOT = Path('C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\')    #windows
# ROOT = '/Users/peaceforlives/Documents/Projects/cyberbullying/'              #mac
CORPUS = Path(ROOT, 'data\\labelled_tweets\\'+data)
RESULTS = Path(ROOT, 'results')
DOC_PATTERN = r'.*\.json'  

target = 'bullying_trace'
corpus = TweetsCorpusReader(CORPUS.__str__(), DOC_PATTERN, bullying_trace = target)        
processed_tweets = corpus.process_tweet()
normalize  = TextNormalizer_lemmatize()
X = list(normalize.fit_transform(processed_tweets)) # X = [' '.join(doc) for doc in normalized_tweets]
y = list(corpus.fields(target))

vectorize = TfidfVectorizer(tokenizer=identity, preprocessor=None, lowercase=False, ngram_range=(1,2))
X_vect = vectorize.fit_transform(X)

labels = LabelEncoder()
y = labels.fit_transform(y)

n = 5000
X_train = X_vect[:n,]
X_test =  X_vect[n:,]
y_train = y[:n]
y_test = y[n:]

train_model(LogisticRegression(), X_train, y_train, X_test, y_test)
train_model(MultinomialNB(), X_train, y_train, X_test, y_test)
train_model(SVC(), X_train, y_train, X_test, y_test)
train_model(SGDClassifier(), X_train, y_train, X_test, y_test)
train_model(GaussianNB(), X_train, y_train, X_test, y_test)
train_model(KNeighborsClassifier(), X_train, y_train, X_test, y_test)
train_model(RandomForestRegressor(), X_train, y_train, X_test, y_test)
# print(clsr(y_test, y_pred))#, target_names=labels.classes_))
# print(cm(y_test, y_pred))#, labels=[1,0]))
# print(accuracy_score(y_test, y_pred))