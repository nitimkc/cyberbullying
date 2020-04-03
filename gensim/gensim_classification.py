# 1. read corpus
# 2. create loader object (iterable of train and test sets)

from reader import TweetsCorpusReader
from loader import CorpusLoader
from transformers import TextNormalizer_lemmatize, GensimVectorizer
from sklearn.preprocessing import LabelEncoder

from pathlib import Path
import numpy as np
import nltk
import os
import json
import logging
import re

log = logging.getLogger("readability.readability")
log.setLevel('WARNING')


ROOT = Path('C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\') # windows
# ROOT = Path('/Users/peaceforlives/Documents/Projects/cyberbullying/')         # mac
CORPUS = Path.joinpath(ROOT, 'data', 'labelled_tweets', 'b')
RESULTS = Path.joinpath(ROOT, 'results')

DOC_PATTERN = r'.*\.json' 

target = 'bullying_trace'
<<<<<<< HEAD
target = 'bullying_role'
target = 'form_of_bullying'
target = 'bullying_post_type'
=======
>>>>>>> 78a41882454b4acb17f8ed2e6e4a30676a7ccf73
if __name__ == '__main__':

    from sklearn.pipeline import Pipeline
    from sklearn.linear_model import LogisticRegression
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.metrics import accuracy_score

    corpus = TweetsCorpusReader(CORPUS.__str__(), DOC_PATTERN, bullying_trace=target)
    docs = corpus.process_tweet()
    labels = list(corpus.fields(target))
<<<<<<< HEAD
    from collections import Counter
    Counter(labels)

    model = Pipeline([
        ('normalizer', TextNormalizer_lemmatize()),
        ('gensim_vect', GensimVectorizer('lexicon.pkl')),
        ('logistic', LogisticRegression())
        # ('bayes', MultinomialNB())
    ])
    model.fit(docs, labels)
    
    normal = TextNormalizer_lemmatize()
    norm_docs = normal.fit_transform(docs)
    gensim = GensimVectorizer('lexicon.pkl')
    gensim_docs = gensim.fit_transform(norm_docs)

    model.predict(gensim_docs)

    clf = LogisticRegression()
    clf.fit(gensim_docs, labels)
    y_pred = clf.predict(gensim_docs)
    accuracy_score(y_pred, labels)

    from gensim.models import Word2Vec
    from gensim.models.phrases import Phraser, Phrases

    common_terms = ["of", "with", "without", "and", "or", "the", "a"]

    # Create the relevant phrases from the list of sentences:
    phrases = Phrases(norm_docs, common_terms=common_terms)
    bigram = Phraser(phrases)

    # Applying the Phraser to transform our sentences is simply
    bigram_docs = list(bigram[norm_docs])
    print(len(bigram_docs))
    print(bigram_docs[-1])

    model = Word2Vec(norm_docs, 
                    min_count=3,   # Ignore words that appear less than this
                    size=200,      # Dimensionality of word embeddings
                    workers=2,     # Number of processors (parallelisation)
                    window=5,      # Context window for words during training
                    iter=30)       # Number of epochs training over corpus
    
    def avg_vec(doc):
        docvec = np.mean( np.array([model[i] for i in doc]), axis=0)
        return doc
    test = [avg_vec(doc) for doc in norm_docs]
=======

   
>>>>>>> 78a41882454b4acb17f8ed2e6e4a30676a7ccf73
