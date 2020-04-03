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

<<<<<<< HEAD
import spacy
from spacymoji import Emoji

=======
>>>>>>> 78a41882454b4acb17f8ed2e6e4a30676a7ccf73
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

<<<<<<< HEAD
    def __init__(self, path=None, library='en_core_web_md'):
        self.path = path
        self.id2word = None
        self.nlp = spacy.load(library) # includes 20k unique vectors with 300 dimensions
=======
    def __init__(self, path=None):
        self.path = path
        self.id2word = None
>>>>>>> 78a41882454b4acb17f8ed2e6e4a30676a7ccf73

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

<<<<<<< HEAD
    # def transform(self, documents):
    #     docvecs = []
    #     for doc in documents:
    #         docvecs.append(self.id2word.doc2bow(doc))
    #     docvecs = [sparse2full(docvec, len(self.id2word)) for docvec in docvecs]
    #     docvec_mat = sp.csr_matrix(docvecs,  dtype=np.float64)
    #     # print(docvec_mat.shape)
    #     return docvec_mat

    # A pre-trained model is a set of word embeddings that have been created elsewhere 
    # that you simply load onto your computer and into memory. They can leverage 
    # massive datasets that you may not have access to that captures word meanings 
    # in a statistically robust manner. The disadvantage of pre-trained word embeddings 
    # is that the words contained within may not capture the peculiarities of language 
    # in your specific application domain. 
    # def transform(self, documents):
    #     emoji = Emoji(self.nlp)
    #     self.nlp.add_pipe(emoji, first=True)

    #     docvecs = []
    #     for doc in documents:
    #         docvec = self.nlp(' '.join(doc))
    #         docvecs.append(docvec.vector)
    #     docvec_mat = sp.csr_matrix(docvecs,  dtype=np.float64)

    #     return docvec_mat

=======
    def transform(self, documents):
        docvecs = []
        for doc in documents:
            docvecs.append(self.id2word.doc2bow(doc))
        docvecs = [sparse2full(docvec, len(self.id2word)) for docvec in docvecs]
        docvec_mat = sp.csr_matrix(docvecs,  dtype=np.float64)
        # print(docvec_mat.shape)
        return docvec_mat
>>>>>>> 78a41882454b4acb17f8ed2e6e4a30676a7ccf73

