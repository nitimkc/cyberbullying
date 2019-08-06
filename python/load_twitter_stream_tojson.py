import tweepy as tw
import json

import twitter_credentials
consumer_key = twitter_credentials.consumerkey
consumer_secret = twitter_credentials.consumersecret
access_token = twitter_credentials.accesstoken
access_secret= twitter_credentials.accesssecret

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

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
        print("Stream Restarted")
 
    def on_data(self, data):
        # connect to your mongoDB and stores the tweet
        try:
    
            # Decode the JSON from Twitter
            datajson = json.loads(data)
            
            # exclude retweets
            if not datajson['text'].startswith('RT'):

                #print(datajson['text'].encode('ascii', 'ignore'))
                # grab the 'created_at' data from the Tweet to use for display
                created_at = datajson['created_at']
                #print("Tweet collected at " + str(created_at))
                #print(str(datajson['created_at']))
                #print(str(datajson['extended_tweet']))

                with open('tweets.json', 'a') as tf:
                    tf.write( json.dump(str(datajson), tf) )

            return True 

        except Exception as e:
           print(e)


listener = StreamListener( api=tw.API(wait_on_rate_limit=True) ) 
streamer = tw.Stream( auth=auth, listener=listener )
print("Tracking: " + str(query))
streamer.filter(track=query, languages=lang)
