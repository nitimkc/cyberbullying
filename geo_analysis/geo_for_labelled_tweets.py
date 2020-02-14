import os
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
            time_loc['timezone'] = tweet['timezone']
            time_loc['localtime'] = tweet['localtime']
            time_loc['state'] = tweet['state']
            path_outfile = Path(RESULTS, 'geotagged_tweets.json')
            with open(path_outfile, 'a') as f:
                f.write(json.dumps(time_loc) + "\n")













import os
import json
import pandas as pd
from pathlib import Path
from geo_analysis import get_timezone

PATH = '/Users/peaceforlives/Documents/Projects/cyberbullying/data/'
input_dir = 'located_tweets'     # data in folder

# files already process should not be processed
files_to_process = list( set( os.listdir(PATH+input_dir) ) - set( os.listdir(PATH+output_dir) ) )
# files_to_process = files_to_process[:20]
file = 'tweets_2019-11-04.json'

for file in files_to_process:
    
    PATH_data = Path(PATH+input_dir)                     # go to input directory
    path_filename = PATH_data.joinpath(PATH_data, file)  # join filename to input directory
    print(path_filename)                                 # print full path of the file being processed
    
    data = []
    with open(path_filename) as f:
        for line in f:
            data.append(json.loads(line))

    for tweet in data:
            if tweet['state']:
                # print(tweet)
                time_loc = { }
                time_loc['id'] = tweet['id']
                time_loc['timezone'] = tweet['id']
                time_loc['localtime'] = tweet['localtime']
                time_loc['state'] = tweet['state']
    
    path_outfile = Path.joinpath(PATH_data.parents[0], output_dir, path_filename.name)
    for tweet in data:
        new_tweet = get_timezone(tweet)
        with open(path_outfile, 'a') as f:
            f.write(json.dumps(new_tweet) + "\n")