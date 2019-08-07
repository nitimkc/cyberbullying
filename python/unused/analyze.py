import pymongo
from pymongo import MongoClient
import pprint

client = MongoClient('mongodb://localhost:27017/twitterdb')
client.list_database_names()

db = client.twitterdb
collection = db.twitter_search
tweets_iterator = collection.find()
for tweet in tweets_iterator:
	print( tweet['created_at'], tweet['text'])