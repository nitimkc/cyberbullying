from reader import TweetsCorpusReader#, PickledCorpusReader

# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction.text import CountVectorizer
# from transformers import TextNormalizer_lemmatize
# from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD, NMF

import nltk
import os
import json
import pickle
import logging
import re

log = logging.getLogger("readability.readability")
log.setLevel('WARNING')

ROOT = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\'
CORPUS = os.path.join(ROOT, 'data\\filtered')
PICKLED = os.path.join(ROOT, 'data\\pickled')

DOC_PATTERN = r'.*\.json' 
PKL_PATTERN = r'.*\.pickle'

file = CORPUS+'\\tweets_2019-09-01.json'
file = PICKLED+'\\random_tweets_2b.pickle'

# read pickled file
if __name__ == '__main__':
    corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN)
    corpus.describes()
    # corpus = PickledCorpusReader(PICKLED)
    # # match the two readers to ensure all the items are imported over.

    # # if bullying_post = 'yes', make it a test set
    # token_tweets = reader.tagged()
    # print(token_tweets[7066])
    
    # processed_token = process_tweet(corpus)
    # print(processed_tokens[7066])
    # # x = processed_tokens[7066]
    # # " ".join([token for (token, tag) in x ])

    # normalize = TextNormalizer_lemmatize()
    # normalized_tweets = list(normalize.fit_transform(processed_tokens))       # this processed removes some of the words based on lemmatization, punctuation and stopwords
    # print(normalized_tweets[7066])                                            # this did not get rid of special characters  

    # docs = [' '.join(doc) for doc in normalized_tweets]

    # count_vect = CountVectorizer(preprocessor=None, lowercase=False)
    # vectors = count_vect.fit_transform(docs)

    # n_topics = 5
    # lda_model = LatentDirichletAllocation(n_components=n_topics)
    # lda_model.fit_transform(vectors)

    # pipe = Pipeline([
    #     ('tfidf', CountVectorizer(tokenizer='words', preprocessor=None, lowercase=False)),
    #     ('model', LatentDirichletAllocation(n_components=n_topics))
    # ])
    # pipe.fit_transform(docs)
    
    # model = Pipeline([
    #     ('gensim_vect', GensimTfidfVectorizer()),
    #     ('lda', ldamodel.LdaTransformer())
    # ])






    # tweets = reader.strings(CORPUS+'\\tweets_2019-09-01.json')
    # tokenized_tweets = reader.tokenized(CORPUS+'\\tweets_2019-09-01.json')
    # modified_tweets = process_tweet(tweets)

    
# modified_tweets = process_tweet(tweets)