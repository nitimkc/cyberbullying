from pathlib import Path
import pandas as pd
import json
import os


# #path_infile = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\data\\filtered\\tweets_2019-09-01.json'
# PATH = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\data\\filtered\\'
# output_dir = 'send_for_label'

# PATH = '/Users/peaceforlives/Documents/Projects/cyberbullying/data/'
# input_dir = 'filtered'
# output_dir = 'send_for_label'
# path_infile = PATH + input_dir + '/tweets_2019-09-01.json'


def sendforlabel_tweets(path_infile, output_dir):

    # PATH
    PATH_data = Path(path_infile)
    
    # load and select reqd columns
    data = pd.read_json(PATH_data, lines=True)
    data_forlabel = data[['id', 'full_tweet']]

    # #.*? - carries out a non-greedy match for a word starting with a hashtag
    # (?=\s|$) - lookahead for the end of the word or end of the sentence
    # http\S+|www.\S+ - carries out a non-greedy match for a word starting with http or www.
    data_forlabel['url'] = data_forlabel.full_tweet.str.findall(r'http\S+|www.\S+(?=\s|$)')
    data_forlabel['url_count'] = data_forlabel.full_tweet.str.findall(r'http\S+|www.\S+(?=\s|$)').str.len()
    data_forlabel = data_forlabel[data_forlabel.url_count == 0 ]   

    data_forlabel['hashtags'] = data_forlabel.full_tweet.str.findall(r'#.*?(?=\s|$)')
    data_forlabel['hashtag_count'] = data_forlabel.full_tweet.str.findall(r'#.*?(?=\s|$)').str.len()
    data_forlabel = data_forlabel[data_forlabel.hashtag_count <= 5 ]    

    data_forlabel['bullying_trace'] = ''
    data_forlabel['bullying_role'] = ''
    data_forlabel['form_of_bullying'] = ''
    data_forlabel['bullying_post_type'] = ''

    # output
    path_outfile = Path.joinpath(PATH_data.parents[1], output_dir,  (PATH_data.stem + '.csv') )
    data_forlabel.to_csv(path_outfile, index=False, encoding = 'utf-8-sig')


#sendforlabel_tweets(path_infile=path_infile , output_dir=output_dir)
