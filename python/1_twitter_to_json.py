import tweepy as tw
import json
from datetime import date
from urllib3.exceptions import ProtocolError

import twitter_credentials
consumer_key = twitter_credentials.consumerkey
consumer_secret = twitter_credentials.consumersecret
access_token = twitter_credentials.accesstoken
access_secret= twitter_credentials.accesssecret


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

query = ['bullied', 'bully','bullying', 'cyberbullied','cyberbully','cyberbullying', '-filter:retweets']#, '-trump '] 
lang = ['en']


class StreamListener(tw.StreamListener):    
    # access the Twitter Streaming API 
    
    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print( 'An Error has occured: ' + repr(status_code) )
        return True
        print('Stream Restarted')
 
    # def on_data(self, data):
    #     try:
    #         filename = 'tweets_' + str(date.today()) + '.json'
    #         with open(filename, 'a') as f:
    #             f.write(data)
    #             #print("Tweet collected at " + str(json.loads(data)['created_at']))
    #             return True

    #     except BaseException as e:
    #         print("Error on_data: %s" % str(e))
    #     return True

    def on_data(self, data):
        try:
    
            # Decode the JSON from Twitter
            datajson = json.loads(data)
            
            # exclude retweets
            if not datajson['text'].startswith('RT'):
                filename = 'tweets_' + str(date.today()) + '.json'
                with open(filename, 'a') as f:
                	f.write(data)
                
                #print("Tweet collected at " + str(json.loads(data)['created_at']))

            return True 

        except Exception as e:
           print(e)




while True:
    try:
        listener = StreamListener( api=tw.API(wait_on_rate_limit=True) ) 
        streamer = tw.Stream( auth=auth, listener=listener )
        streamer.filter(track=query, languages=lang, stall_warnings=True)
        print("Tracking: " + str(query))
    except Exception as e:
        print e
        pass