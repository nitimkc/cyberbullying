import pandas as pd 
import os
import json

PATH = '/Users/peaceforlives/Documents/Projects/cyberbullying/data/'
infile = 'raw/'
outfile ='no_retweets/'

# only applicable for the files mentioned heres
files = ['tweets_2019-08-19.json', 'tweets_2019-08-20.json', 'tweets_2019-08-21.json']
filename = files[0]

data = pd.read_json(PATH + infile + filename, orient='records', lines=True)
print(data.head())

#data = pd.read_json(PATH + infile + filename)
#print(data.head())
df = data[-data.text.str.startswith(('RT'))]
df.to_json(PATH + outfile + filename, orient='records', lines=True)

infile='no_retweets/'
data = pd.read_json(PATH + infile + filename, orient='records', lines=True)
data.head()

#remove_tweets(PATH=PATH, infile=infile, outfile=outfile, filename=filename)

# for file in os.listdir(PATH + infile):
#     remove_tweets(PATH=PATH, infile=infile, outfile=outfile, filename=file)
#     #print(file)

