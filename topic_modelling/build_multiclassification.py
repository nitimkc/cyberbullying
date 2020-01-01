# 1. create pipeline of normalizer and vectorizer
# 2. apply pipeline to each classification model 
# 3. function to store model scores

import nltk
nltk.download('stopwords')
import unicodedata
import numpy as np
import time
import json

# from reader import TweetsCorpusReader
# from loader import CorpusLoader

from transformers import TextNormalizer_lemmatize, GensimVectorizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

from sklearn.linear_model import SGDClassifier
from sklearn.decomposition import TruncatedSVD

from sklearn.pipeline import Pipeline

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def identity(words):
    return words

def create_pipeline(estimator, reduction=False):

    steps = [
        ('normalize', TextNormalizer_lemmatize()),
        # ('vectorize', CountVectorizer(
        #     ngram_range=(1, 4), analyzer='char', lowercase=False
        # ))
        ('ngram_vect', TfidfVectorizer(
            tokenizer=identity, preprocessor=None, lowercase=False, ngram_range=(1,2)
        ))        
    ]

    if reduction:
        steps.append((
            'reduction', TruncatedSVD(n_components=600)
        ))

    # Add the estimator
    steps.append(('classifier', estimator))

    return Pipeline(steps)


models = []
# models.append(create_pipeline(GaussianNB(), False))
models.append(create_pipeline(LogisticRegression(solver='newton-cg',multi_class="multinomial"), False))
models.append(create_pipeline(SVC(kernel='linear'), False))
models.append(create_pipeline(KNeighborsClassifier(n_neighbors = 8), False))


def score_models(models, loader):
    for model in models:

        name = model.named_steps['classifier'].__class__.__name__
        if 'reduction' in model.named_steps:
            name += " (TruncatedSVD)"

        scores = {
            'model': str(model),
            'name': name,
            'accuracy': [],
            'precision': [],
            'recall': [],
            'f1': [],
            'time': [],
        }

        for X_train, X_test, y_train, y_test in loader:
            start = time.time()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            # print(y_pred)

            scores['time'].append(time.time() - start)
            scores['accuracy'].append(accuracy_score(y_test, y_pred))
            scores['precision'].append(precision_score(y_test, y_pred, average='weighted'))
            scores['recall'].append(recall_score(y_test, y_pred, average='weighted'))
            scores['f1'].append(f1_score(y_test, y_pred, average='weighted'))
            print(scores)

        yield scores

# if __name__ == '__main__':
#     for scores in score_models(models, loader):
#         with open('results.json', 'a') as f:
#             f.write(json.dumps(scores) + "\n")

# for X_train, X_test, y_train, y_test in loader:
#     train_x = X_train
#     train_y = y_train
#     test_x = X_test
#     test_y = y_train
#     print(len(x))