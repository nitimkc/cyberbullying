import json
from pymongo import MongoClient


# connect to your mongoDB and stores the tweet
mongo_host = 'mongodb://localhost:27017/twitterdb'
client = MongoClient(mongo_host)
db = client.tweets

import json    

data = []
with open('tweets.json', encoding='utf-8') as f:
    for line in f:
        data.append(json.loads(line))

data 

