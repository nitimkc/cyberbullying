# 1. read corpus
# 2. create loader object (iterable of train and test sets)

from reader import TweetsCorpusReader
from loader import CorpusLoader
from transformers import TextNormalizer, GensimTfidfVectorizer
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


# ROOT = Path('C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\') # windows
ROOT = Path('/Users/peaceforlives/Documents/Projects/cyberbullying/')         # mac
CORPUS = Path.joinpath(ROOT, 'data', 'labelled_tweets', 'ab')
RESULTS = Path.joinpath(ROOT, 'results')

DOC_PATTERN = r'.*\.json' 


##########################################################################
## binary-classification
##########################################################################
target = 'bullying_trace'
# target = 'bullying_role'
# target = 'form_of_bullying'
# target = 'bullying_post_type'
if __name__ == '__main__':

    from sklearn.pipeline import Pipeline
    from sklearn.linear_model import LogisticRegression
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.metrics import accuracy_score
    from sklearn.metrics import f1_score
    from sklearn.model_selection import train_test_split as tts
    from sklearn.preprocessing import LabelEncoder

    corpus = TweetsCorpusReader(CORPUS.__str__(), DOC_PATTERN, bullying_trace=target)
    docs = corpus.process_tweet()
    y = list(corpus.fields(target))
    from collections import Counter
    Counter(y)
    labels = LabelEncoder()
    y = labels.fit_transform(y)
    # model = Pipeline([
    #     ('normalizer', TextNormalizer()),
    #     ('gensim_vect', GensimVectorizer('lexicon.pkl')),
    #     ('logistic', LogisticRegression())
    #     # ('bayes', MultinomialNB())
    # ])
    # model.fit(docs, labels)
    # model.predict(gensim_docs)
    
    normal = TextNormalizer()
    norm_docs = list(normal.fit_transform(docs))
    gensim = GensimTfidfVectorizer()
    gensim_docs = gensim.fit_transform(norm_docs)
    gensim_docs

    X_train, X_test, y_train, y_test = tts(gensim_docs, y, test_size=0.2)

    clf = LogisticRegression()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    f1_score(y_pred, y_test)
    accuracy_score(y_pred, y_test)

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
