##########################################################################
## transformers.py
##########################################################################

# !/usr/bin/env python3

import os
import nltk
import gensim
import unicodedata
import string 

# from loader import CorpusLoader
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

from nltk.stem import SnowballStemmer

from sklearn.base import BaseEstimator, TransformerMixin
from gensim.matutils import sparse2full

class TextNormalizer_lemmatize(BaseEstimator, TransformerMixin):

    def __init__(self, language='english'):
        self.stopwords  = set(nltk.corpus.stopwords.words(language))
        self.lemmatizer = WordNetLemmatizer()

    def is_punct(self, token):
        return all(
            unicodedata.category(char).startswith('P') for char in token
        )

    def is_stopword(self, token):
        return token.lower() in self.stopwords

    def normalize(self, document):
        return [
            self.lemmatize(token, tag).lower()
            for (token, tag) in document
            if not self.is_punct(token) #and not self.is_stopword(token)
        ]

    def lemmatize(self, token, pos_tag):
        tag = {
            'N': wn.NOUN,
            'V': wn.VERB,
            'R': wn.ADV,
            'J': wn.ADJ
        }.get(pos_tag[0], wn.NOUN)

        return self.lemmatizer.lemmatize(token, tag)

    def fit(self, X, y=None):
        return self

    def transform(self, documents):
        for document in documents:
            yield self.normalize(document)


class TextNormalizer_stem(BaseEstimator, TransformerMixin):
    
    # Initialization function
    def __init__(self, language='english'):
        self.stopwords = set(nltk.corpus.stopwords.words(language))
        self.stemmer = SnowballStemmer(language)
    
    def is_punct(self, token):
        return all(unicodedata.category(char).startswith('P') for char in token)
    
    def is_stopword(self, token):
        return token.lower() in self.stopwords
    
    def normalize(self, document):
        return [
            self.stemmize(token, tag).lower()
            for (token, tag) in document
            if not self.is_punct(token) and not self.is_stopword(token)
        ]
    
    def stemmize(self, token, pos_tag):
        return self.stemmer.stem(token.lower())
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, documents):
        for document in documents:
            yield self.normalize(document)


# class GensimVectorizer(BaseEstimator, TransformerMixin):

#     def __init__(self, path=None):
#         self.path = path
#         self.id2word = None

#         self.load()

#     def load(self):
#         if os.path.exists(self.path):
#             self.id2word = gensim.corpora.Dictionary.load(self.path)

#     def save(self):
#         self.id2word.save(self.path)

#     def fit(self, documents, labels=None):
#         self.id2word = gensim.corpora.Dictionary(documents)
#         self.save()

#     def transform(self, documents):
#         for document in documents:
#             for tweet in document:
#                 tweetvec = self.id2word.doc2bow(tweet)
#                 yield sparse2full(tweetvec, len(self.id2word))
import scipy.sparse as sp
class GensimVectorizer(BaseEstimator, TransformerMixin):

    def __init__(self, path=None):
        self.path = path
        self.id2word = None

        self.load()

    def load(self):
        if os.path.exists(self.path):
            self.id2word = gensim.corpora.Dictionary.load(self.path)

    def save(self):
        self.id2word.save(self.path)

    def fit(self, documents, labels=None):
        self.id2word = gensim.corpora.Dictionary(documents)
        self.save()

    # def transform(self, documents):
    #     for document in documents:
    #             tweetvec = self.id2word.doc2bow(document)
    #             yield sparse2full(tweetvec, len(self.id2word))

    def transform(self, documents):
        tweetvec = []
        for tweet in documents:
            tweetvec.append(self.id2word.doc2bow(tweet))
        docvec = [sparse2full(tweet, len(self.id2word)) for tweet in tweetvec]
        return sp.csr_matrix(docvec)

