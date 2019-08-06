import json
from pymongo import MongoClient


# connect to your mongoDB and stores the tweet
mongo_host = 'mongodb://localhost:27017/twitterdb'
client = MongoClient(mongo_host)
db = client.tweets

with open('tweets.json', 'r') as f:
    tweets_dict = json.load(f)

db.tweets_collection.insert(tweets_dict)

