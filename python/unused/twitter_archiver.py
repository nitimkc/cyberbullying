from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import AppAuthHandler
from tweepy import Stream
 
import app_credentials
import tweepy
import numpy as np 
import pandas as pd 



auth = tweepy.AppAuthHandler(app_credentials.consumerkey, app_credentials.consumersecret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)


#Getting Geo ID for Canada
places = api.geo_search(query="Canada", granularity="country")    

#Copy USA id
place_id = places[0].id
print('Canada id is: ',place_id)


searchQuery = '"bully" OR "bullied" OR "bullying"' 

#Maximum number of tweets we want to collect 
maxTweets = 500

#The twitter Search API allows up to 100 tweets per query
tweetsPerQry = 100

tweetCount = 0

#Open a text file to save the tweets to
with open('cyberbully.json', 'w') as f:

    #Tell the Cursor method that we want to use the Search API (api.search)
    #Also tell Cursor our query, and the maximum number of tweets to return
    for tweet in tweepy.Cursor(api.search,q=searchQuery).items(maxTweets) :         

        #Verify the tweet has place info before writing (It should, if it got past our place filter)
        if tweet.place is not None:
            
            #Write the JSON format to the text file, and add one to the number of tweets we've collected
            f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
            tweetCount += 1

    #Display how many tweets we have collected
    print("Downloaded {0} tweets".format(tweetCount))