import pandas as pd
import json
import os

PATH = '/Users/peaceforlives/Documents/Projects/cyberbullying/data/'
path = r'/Users/peaceforlives/Documents/Projects/cyberbullying/data/'
infile = 'filtered/'
outfile = 'send_for_label/'
filename = 'tweets.json'

def sendforlabel_tweets(PATH, infile, outfile, filename):
    
    # load and select reqd columns
    data = pd.read_json(PATH + infile + filename, lines=True)
    data_forlabel = data[['id', 'full_tweet']]
    data_forlabel['no_hashtags'] = 
    #print(data_forlabel.head())

    data_forlabel.to_csv(path + outfile + filename.rsplit('.',1)[0] + '.csv', index=False, encoding = 'utf-8-sig', )

for file in os.listdir(PATH + infile):
    print(file)
    sendforlabel_tweets(PATH=PATH, infile=infile, outfile=outfile, filename=file)
    


