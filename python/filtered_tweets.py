from pathlib import Path
import pandas as pd
import json
import os

# #path_infile = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\data\\original\\tweets_2019-09-01.json'
# PATH = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\data\\original\\'
# keywords = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\python\\secondary_keywords.txt'

# primary = '/Users/peaceforlives/Documents/Projects/cyberbullying/python/primary_keywords.txt' 
# secondary = '/Users/peaceforlives/Documents/Projects/cyberbullying/python/secondary_keywords.txt' 
# additional = '/Users/peaceforlives/Documents/Projects/cyberbullying/python/additional_keywords.txt' 
# PATH = '/Users/peaceforlives/Documents/Projects/cyberbullying/data/'
# input_dir = 'original'
# output_dir = 'filtered'
# path_infile = PATH + input_dir + '/tweets_2019-09-01.json'
# keywords = primary
# keywords = secondary
# keywords = additional


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

    # PATH
    PATH_data = Path(path_infile)
    primary = Path(primary)
    secondary = Path(secondary)
    additional = Path(additional)
 
    # load and select reqd columns
    data = pd.read_json(PATH_data, lines=True)
    cols = ['created_at', 'id', 'text', 'source', 'geo', 'coordinates', 'place', 'lang', 'extended_tweet']
    data = data[cols]

    # extract full txt of extnd tweets
    data['full_tweet'] =  data['extended_tweet'].apply(pd.Series)['full_text']
    data['full_tweet'].fillna(data.text, inplace=True)
    data.drop(['text', 'extended_tweet'], axis=1, inplace=True)

    # load primary keywords
    primaryfilter_data = filter_keywords(data=data, keywords=primary)
    secondaryfilter_data = filter_keywords(data=primaryfilter_data, keywords=secondary)
    additionalfilter_data = filter_keywords(data=secondaryfilter_data, keywords=additional, omit=True)


    # output
    path_outfile = Path.joinpath(PATH_data.parents[1], output_dir, PATH_data.name)
    additionalfilter_data.to_json( path_outfile, orient='records', lines=True)


#filtered_tweets(path_infile, primary, secondary, additional, output_dir)


