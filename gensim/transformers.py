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
import numpy as np
import scipy.sparse as sp

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
        # for document in documents:
            # yield self.normalize(document)
        norm_tweet = []
        for document in documents:
            norm_tweet.append(self.normalize(document))
        return norm_tweet


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
        return self

    # def transform(self, documents):
    #     print(documents)
    #     for document in documents:
    #         docvec = self.id2word.doc2bow(document)
    #         docvec = sparse2full(docvec, len(self.id2word)) 
    #         # docvec = sp.csr_matrix(docvec, dtype=np.float64)
    #         # print(docvec)
    #         yield docvec

    def transform(self, documents):
        docvecs = []
        for doc in documents:
            docvecs.append(self.id2word.doc2bow(doc))
        docvecs = [sparse2full(docvec, len(self.id2word)) for docvec in docvecs]
        docvec_mat = sp.csr_matrix(docvecs,  dtype=np.float64)
        # print(docvec_mat.shape)
        return docvec_mat

