import os
import json
from pathlib import Path
from reader import TweetsCorpusReader
from timezonefinder import TimezoneFinder


#windows
# ROOT = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\'
# CORPUS = os.path.join(ROOT, 'data\\original') #labelled_tweets\\ab')
# RESULTS = os.path.join(ROOT, 'results')

#mac
ROOT = '/Users/peaceforlives/Documents/Projects/cyberbullying/'
CORPUS = os.path.join(ROOT, 'data/located_tweets')
RESULTS = os.path.join(ROOT, 'data/geotagged_tweets')

DOC_PATTERN = r'.*\.json' 

if __name__ == '__main__':
    corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN) #, bullying_trace='coordinates')  # geo: lat, lon, coordinates: lon, lat
    docs = corpus.docs()

    for tweet in docs:
        if tweet['state']:
            time_loc = { }
            time_loc['id'] = tweet['id']
            time_loc['full_tweet'] = tweet['full_tweet']
            time_loc['timezone'] = tweet['timezone']
            time_loc['localtime'] = tweet['localtime']
            time_loc['state'] = tweet['state']
            path_outfile = Path(RESULTS, 'geotagged_tweets.json')
            with open(path_outfile, 'a') as f:
                f.write(json.dumps(time_loc) + "\n")
