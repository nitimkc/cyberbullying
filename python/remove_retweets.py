import pandas as pd 
import os
import json

# remove retweets for file in test folder and export result to no_retweets

PATH = '/Users/peaceforlives/Documents/Projects/cyberbullying/data/'
infile = 'test/'
outfile='no_retweets/'
filename='tweets_some.json'

def remove_tweets(PATH, infile, outfile, filename):

    data = pd.read_json(PATH + infile + filename, orient='records', lines=True)
    #data = pd.read_json(PATH + infile + filename)

    df = data[-data.text.str.startswith(('RT'))]
    df.to_json(PATH + outfile + filename, orient='records', lines=True)

#remove_tweets(PATH=PATH, infile=infile, outfile=outfile, filename=filename)

for file in os.listdir(PATH + infile):
    remove_tweets(PATH=PATH, infile=infile, outfile=outfile, filename=file)
    #print(file)