import tweepy as tw
import json

from pymongo import MongoClient
mongo_host = 'mongodb://localhost:27017/twitterdb'

import twitter_credentials
consumer_key = twitter_credentials.consumerkey
consumer_secret = twitter_credentials.consumersecret
access_token = twitter_credentials.accesstoken
access_secret= twitter_credentials.accesssecret


query = ['bullied', 'bully','bullying', 'cyberbullied','cyberbully','cyberbullying']#, '-trump '] 
lang = ['en']
 
class StreamListener(tw.StreamListener):    
    # access the Twitter Streaming API 

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return True
        print ("Stream Restarted")
 
    def on_data(self, data):
        # connect to your mongoDB and stores the tweet
        try:
            client = MongoClient(mongo_host)
            
            # Use twitterdb database. If it doesn't exist, it will be created.
            db = client.twitterdb
    
            # Decode the JSON from Twitter
            datajson = json.loads(data)
            # exclude retweets
            if not datajson['text'].startswith('RT'):

                #print(datajson['text'].encode('ascii', 'ignore'))

                # grab the 'created_at' data from the Tweet to use for display
                created_at = datajson['created_at']

                # print out a message to the screen that we have collected a tweet
                print("Tweet collected at " + str(created_at))
    
                # insert the data into the mongoDB as collection-twitter_search
                # if it doesn't exist, it will be created
                db.twitter_search.insert(datajson)
            return True 

        except Exception as e:
           print(e)


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# Set up the listener
# 'wait_on_rate_limit=True' to help with Twitter API rate limiting

listener = StreamListener(api=tw.API(wait_on_rate_limit=True)) 
streamer = tw.Stream(auth=auth, listener=listener)
print("Tracking: " + str(query))
streamer.filter(track=query, languages=lang)
