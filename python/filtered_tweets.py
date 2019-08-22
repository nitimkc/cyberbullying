import pandas as pd
import json
import os

PATH = '/Users/peaceforlives/Documents/Projects/cyberbullying/data/'
infile = 'original/'
outfile = 'filtered/'
filename = 'tweets_2019-08-14.json'

def filtered_tweets(PATH, infile, outfile, filename):
    
    # load and select reqd columns
    data = pd.read_json(PATH + infile + filename, lines=True)
    cols = ['created_at', 'id', 'text', 'source', 'geo', 'coordinates', 'place', 'lang', 'extended_tweet']
    data = data[cols]

    # extract full txt of extnd tweets
    data['full_tweet'] =  data['extended_tweet'].apply(pd.Series)['full_text']
    data['full_tweet'].fillna(data.text, inplace=True)
    data.drop(['text', 'extended_tweet'], axis=1, inplace=True)

    # load secondary keywords
    secondary_filter = open('secondary_keywords.txt', 'r', newline='')
    match = secondary_filter.read().splitlines()

    # search for secondary keywords in full text tweets
    data['full_tweet'] = data['full_tweet'].str.lower()
    matched_idx = data['full_tweet'].str.contains('|'.join(match), case=False)
    matched_data  = data[matched_idx]
    matched_data.to_json(PATH + outfile + filename, orient='records', lines=True)

    #review_data = 
    #review_data.to_csv( r'%s' % PATH + outfile + filename.rsplit('.',1)[0] + '.csv')

for file in os.listdir(PATH + infile):
    print(file)
    filtered_tweets(PATH=PATH, infile=infile, outfile=outfile, filename=file)
    


