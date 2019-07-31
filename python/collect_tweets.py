import pymongo
from pymongo import MongoClient
import json
import twitter as tw 
from pprint import pprint

import twitter_credentials

auth = tw.OAuthHandler(twitter_credentials.consumerkey, twitter_credentials.consumersecret)
auth.set_access_token(twitter_credentials.accesstoken, twitter_credentials.accesssecret)
twitter_api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

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
 
q = "bullied OR bully OR bullyed lang:en"
  
'''
fetch data
'''
  
search_results = twitter_api.search.tweets( count=count,q=q)
# pprint(search_results['search_metadata'])
         
statuses = search_results["statuses"]


since_id_new = statuses[-1]['id']

for statuse in statuses:

    try:
        tweet_collection.insert(statuse)
#         pprint(statuse['created_at'])
  
    except:
        pass

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

    for statuse in statuses:
                
        try:
            tweet_collection.insert(statuse)
#             pprint(statuse['created_at'])
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