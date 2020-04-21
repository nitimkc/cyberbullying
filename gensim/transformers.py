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
from gensim.corpora import Dictionary
from gensim.models.tfidfmodel import TfidfModel
from gensim.models.doc2vec import TaggedDocument, Doc2Vec

import numpy as np
import scipy.sparse as sp

# import spacy
# from spacymoji import Emoji

class TextNormalizer(BaseEstimator, TransformerMixin):

    def __init__(self, language='english', lemma=True):
        self.lemmate = lemma 
        self.stopwords  = set(nltk.corpus.stopwords.words(language))
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = SnowballStemmer(language)

    def is_punct(self, token):
        return all(
            unicodedata.category(char).startswith('P') for char in token
        )

    def is_stopword(self, token):
        return token.lower() in self.stopwords

    def lemmatize(self, token, pos_tag):
        tag = {
            'N': wn.NOUN,
            'V': wn.VERB,
            'R': wn.ADV,
            'J': wn.ADJ
        }.get(pos_tag[0], wn.NOUN)

        return self.lemmatizer.lemmatize(token, tag)

    def normalize_lemm(self, document):
        return [
            self.lemmatize(token, tag).lower()
            for (token, tag) in document
            if not self.is_punct(token) #and not self.is_stopword(token)
        ]
    
    def stemmize(self, token, pos_tag):
        return self.stemmer.stem(token.lower())

    def normalize_stem(self, document):
        return [
            self.stemmize(token, tag).lower()
            for (token, tag) in document
            if not self.is_punct(token) and not self.is_stopword(token)
        ]

    def fit(self, X, y=None):
        return self

    def transform(self, documents):
        for document in documents:
            if self.lemmate:
                yield self.normalize_lemm(document)
            else:
                yield self.normalize_stem(document)

    # def transform(self, documents):
    #     norm_tweet = []
    #     for document in documents:
    #         if self.lemmate:
    #             norm_tweet.append(self.normalize_lemm(document))
    #         else:
    #             norm_tweet.append(self.normalize_stem(document))  
    #     return norm_tweet



class GensimTfidfVectorizer(BaseEstimator, TransformerMixin):

    def __init__(self, dirpath=".", type='tfidf', tofull=False, vec_size=100):
        """
        Pass in a directory that holds the lexicon in corpus.dict and the
        TFIDF model in tfidf.model (for now).
        Set tofull = True if the next thing is a Scikit-Learn estimator
        otherwise keep False if the next thing is a Gensim model.
        """
        self._type = type
        self._lexicon_path = os.path.join(dirpath, "corpus.dict")
        self._model_path = os.path.join(dirpath, type+".model")
        self.lexicon = None
        self.model = None
        self.tofull = tofull
        self._nfeat = vec_size

        self.load()

    def load(self):

        if os.path.exists(self._lexicon_path):
            self.lexicon = Dictionary.load(self._lexicon_path)

        if os.path.exists(self._model_path):
            self.model = TfidfModel().load(self._model_path)

    def save(self):
        self.lexicon.save(self._lexicon_path)
        self.model.save(self._model_path)

    def fit(self, documents, labels=None):
        if self._type=="tfidf":
            self.lexicon = Dictionary(documents)
            self.model = TfidfModel( [self.lexicon.doc2bow(doc) for doc in documents], id2word=self.lexicon )
        self.save()
        return self

    def transform(self, documents):
        if self._type=="doc2vec":
            taggeddoc = [ TaggedDocument(words, ['d{}'.format(idx)]) for idx, words in enumerate(documents) ]
            model = Doc2Vec( taggeddoc, vector_size=self._nfeat, window=2, min_count=1, workers=4)
            docvec_mat = self.model.docvecs.vectors_docs 
        else:
            if self._type=="count":
                docvecs = [ self.lexicon.doc2bow(document) for document in documents]
            elif self._type=="ohe":
                docvecs = [ [(token[0], 1) for token in self.lexicon.doc2bow(document)] for document in documents ]
            else: 
                docvecs = [ self.tfidf[self.lexicon.doc2bow(document)] for document in documents ]
            docvecs = [ sparse2full(docvec, len(self.lexicon)) for docvec in docvecs ]
            docvec_mat = sp.csr_matrix(docvecs, dtype=np.float64)
        return docvec_mat

    # def transform(self, documents):
    #     for document in documents:
    #         docvec = self.id2word.doc2bow(document)
    #         docvec = sparse2full(docvec, len(self.id2word)) 
    #         docvec = sp.csr_matrix(docvec, dtype=np.float64)
    #         # print(docvec)
    #         yield docvec

    # def transform(self, documents):
    #     def generator():
    #         for document in documents:
    #             vec = self.tfidf[self.lexicon.doc2bow(document)]
    #             if self.tofull:
    #                 yield sparse2full(vec, len(self.lexicon))
    #             else:
    #                 yield vec
    #     return list(generator())


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










