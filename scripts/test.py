from wordcloud import WordCloud
from reader import TweetsCorpusReader
from loader import CorpusLoader

from sklearn.model_selection import train_test_split as tts
from build import models
from build import score_models

from sklearn.pipeline import Pipeline
from transformers import TextNormalizer_lemmatize

import nltk
import os
import json
import pickle
import logging
import re

log = logging.getLogger("readability.readability")
log.setLevel('WARNING')

ROOT = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\'
CORPUS = os.path.join(ROOT, 'data\\labelled_tweets')
RESULTS = os.path.join(ROOT, 'results')
DOC_PATTERN = r'.*\.json' 
file = CORPUS+'\\random_tweets_2b.json'

# PICKLED = os.path.join(ROOT, 'data\\pickled\\labelled_tweets')
# PKL_PATTERN = r'.*\.pickle'
# file = PICKLED+'\\random_tweets_2b.pickle'


if __name__ == '__main__':
    corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN)
    processed_tokens = corpus.process_tweet()
    normalize = TextNormalizer_lemmatize()
    normalized_tweets = list(normalize.fit_transform(processed_tokens))

    # Join the different processed titles together.
    long_string = [' '.join(doc) for doc in normalized_tweets ] 

    # Create a WordCloud object
    wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')

    # Generate a word cloud
    wordcloud.generate(long_string)# Visualize the word cloud
    wordcloud.to_image()