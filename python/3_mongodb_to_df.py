# before running this code run the code below on terminal to ensure latest data is loaded
# mongoimport -d tweets -c tweets_collection tweets.json

import pymongo
import pandas as pd
from pymongo import MongoClient

client=MongoClient()
db=client.tweetdb; collection=db.tweets
#db=client.tweets; collection=db.tweets_collection

data=pd.DataFrame( list(collection.find()) )
print( data.tail(10) )

#print ("total docs in collection:", collection.count_documents( {} ))

test = data[-data['text'].str.match('RT')]


db =client.tweet_noRT; collection=db.tweets
data_noRT = test.to_dict(orient='records')
db['tweet_noRT']['tweets'].insert(data_noRT) 