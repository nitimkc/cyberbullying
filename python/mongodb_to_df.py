import pymongo
import pandas as pd
from pymongo import MongoClient

client=MongoClient()
db=client.twitterdb
collection=db.twitter_search

data=pd.DataFrame(list(collection.find()))
print(data.head(10))