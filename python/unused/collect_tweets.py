import pymongo
from pymongo import MongoClient
import json
import twitter as tw 
from pprint import pprint
import pandas as pd
#import twitter_credentials

auth = tw.oauth.OAuth("256116632-DPKz8nJF3yH2898idMhvtMSI7f1fSvGkuKYvsaD5",
"u26R9cFOCrglTg2dxLOXxJG059jf0jjCEem5AroH0HU3r",
"IIag1JQPRgYCN1bgBYbSytErS",
"cMpYi152iEl4LoQqFBB8gx9lDmTzENKXqKh2c0sHkmRrwztabX")
twitter_api = tw.Twitter(auth=auth)

'''
connect mongodb database
'''
client = MongoClient()
db = client.twitterdb
tweet_collection = db.tweet_collection
tweet_collection.create_index([("id", pymongo.ASCENDING)],unique = True) # make sure the collected tweets are unique

'''
define query in REST API
'''
 
count = 100
 
q = "bullied OR bully OR bullying OR cyberbullied OR cyberbully OR cyberbullying -trump lang:en"
  
'''
fetch data
'''
  
search_results = twitter_api.search.tweets( count=count,q=q)
# pprint(search_results['search_metadata'])
         
statuses = search_results["statuses"]


since_id_new = statuses[-1]['id']

# for status in statuses:

#     try:
# #        tweet_collection.insert(status)
#         pprint(status['created_at'])
  
#     except:
#         pass

'''
continue fetching previous data with the same query
YOU WILL REACH YOUR RATE LIMIT VERY FAST
'''   
since_id_old = 0
while(since_id_new != since_id_old):
#     pprint(search_results['search_metadata'])
    since_id_old = since_id_new
    search_results = twitter_api.search.tweets( count=count,q=q, max_id= since_id_new)
    statuses = search_results["statuses"]

    since_id_new = statuses[-1]['id']

    for status in statuses:
                
        try:
#            tweet_collection.insert(status)
            pprint(status['created_at'])
        except:
            pass
#         
 
 
'''
query collected data in MongoDB
'''
 
tweet_cursor = tweet_collection.find()
  
print (tweet_cursor.count())
  
user_cursor = tweet_collection.distinct("user.id")
 
print (len(user_cursor))
 
 
  
for document in tweet_cursor:
    try:
        print ('----')
#         pprint (document)
 
  
        print ('name:', document["user"]["name"])
        print ('text:', document["text"])
    except:
        print ("***error in encoding")
        pass