from pathlib import Path
import pandas as pd
import json
import os

# path_infile = path_filename


def filter_keywords(data, keywords, omit=False):

    # load primary keywords
    filter = open(keywords, 'r', newline='')
    match = filter.read().splitlines()
    filter.close()

    # search for secondary keywords in full text tweets
    data['full_tweet'] = data['full_tweet'].str.lower()
    to_match = '\\b(' + '|'.join(match) + ')\\b'
    matched_idx = data['full_tweet'].str.contains(to_match, case=False)

    # decision based on whether the match is to be included or excluded 
    if omit==True:
        matched_data  = data[-matched_idx]
    else:
        matched_data = data[matched_idx]

    return matched_data

def filtered_tweets(path_infile, primary, secondary, additional, output_dir):
 
    # load and select reqd columns
    data = pd.read_json(path_infile, lines=True)
    cols = ['created_at', 'id', 'text', 'source', 'geo', 'coordinates', 'place', 'lang', 'extended_tweet']
    data = data[cols]
    data['created_at'] = data['created_at'].astype(str)+'+00:00'

    # extract full txt of extnd tweets
    data['full_tweet'] =  data['extended_tweet'].apply(pd.Series)['full_text']
    data['full_tweet'].fillna(data.text, inplace=True)
    data.drop(['text', 'extended_tweet'], axis=1, inplace=True)

    # load primary keywords
    primaryfilter_data = filter_keywords(data=data, keywords=primary)
    secondaryfilter_data = filter_keywords(data=primaryfilter_data, keywords=secondary)
    additionalfilter_data = filter_keywords(data=secondaryfilter_data, keywords=additional, omit=True)

    # output
    path_outfile = Path.joinpath(output_dir, path_infile.name)
    additionalfilter_data.to_json( path_outfile, orient='records', lines=True)


# filtered_tweets(path_infile, primary, secondary, additional, output_dir)


