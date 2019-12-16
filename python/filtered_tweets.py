from pathlib import Path
import pandas as pd
import json
import os
   

def filtered_tweets(path_infile, keywords, output_dir):

    # PATH
    PATH_data = Path(path_infile)
    keywords = Path(keywords)

    # load and select reqd columns
    data = pd.read_json(PATH_data, lines=True)
    cols = ['created_at', 'id', 'text', 'source', 'geo', 'coordinates', 'place', 'lang', 'extended_tweet']
    data = data[cols]

    # extract full txt of extnd tweets
    data['full_tweet'] =  data['extended_tweet'].apply(pd.Series)['full_text']
    data['full_tweet'].fillna(data.text, inplace=True)
    data.drop(['text', 'extended_tweet'], axis=1, inplace=True)

    # load secondary keywords
    secondary_filter = open(keywords, 'r', newline='')
    match = secondary_filter.read().splitlines()

    # search for secondary keywords in full text tweets
    data['full_tweet'] = data['full_tweet'].str.lower()
    matched_idx = data['full_tweet'].str.contains('|'.join(match), case=False)
    matched_data  = data[matched_idx]

    # output
    path_outfile = Path.joinpath(PATH_data.parents[1], output_dir, PATH_data.name)
    matched_data.to_json( path_outfile, orient='records', lines=True)


#path_infile = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\data\\original\\tweets_2019-09-01.json'
PATH = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\data\\original\\'
keywords = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\python\\secondary_keywords.txt'
output_dir = 'filtered'

for file in os.listdir(PATH):
    path_filename = Path.joinpath(PATH_data.parent, file) 
    print(path_filename)
    filtered_tweets( path_filename, keywords, output_dir )

