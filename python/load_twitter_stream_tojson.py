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

reqd_fields = [u'_id', u'created_at',	u'id',	u'text',	u'truncated',	u'geo',	u'coordinates',	u'place',	u'lang',	u'timestamp_ms',	u'extended_tweet',	u'extended_entities',	u'possibly_sensitive',	u'in_reply_to_status_id', u'metadata' ]

tweets = open('today.txt','a')

class StreamListener(tw.StreamListener):    
    # access the Twitter Streaming API 
    
    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return True
        print('Stream Restarted')
 
    def on_data(self, data):
        try:
    
            # Decode the JSON from Twitter
            datajson = json.loads(data)
            
            # exclude retweets
            if not datajson['text'].startswith('RT'):

                print(datajson['text'].encode('ascii', 'ignore'))

                # grab the 'created_at' data from the Tweet to use for display
                created_at = datajson['created_at']
                print("Tweet collected at " + str(created_at))
                
                # save remaining tweets
                tweets.write(str(datajson))

            return True 

        except Exception as e:
           print(e)


listener = StreamListener( api=tw.API(wait_on_rate_limit=True) ) 
streamer = tw.Stream( auth=auth, listener=listener )
print("Tracking: " + str(query))
streamer.filter(track=query, languages=lang)
