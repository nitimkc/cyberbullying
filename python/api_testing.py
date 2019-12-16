import twitter_credentials_fullarchive as cred
import base64
import requests

consumer_key = cred.consumerkey
consumer_secret = cred.consumersecret
access_token = cred.accesstoken
access_secret= cred.accesssecret

key_secret = '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

auth_data = {'grant_type': 'client_credentials'}
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
auth_resp.status_code
# Keys in data response are token_type (bearer) and access_token (your access token)
auth_resp.json().keys()

access_token = auth_resp.json()['access_token']
search_headers = {'Authorization': 'Bearer {}'.format(access_token)}

query = ['bullied', 'bully','bullying', 'cyberbullied','cyberbully','cyberbullying', '-filter:retweets']#, '-trump '] 
lang = ['en']
search_params = {'query': query}  
search_url = '{}1.1/tweets/search/fullarchive/fullSearchSandbox.json'.format(base_url)
search_resp = requests.get(search_url, headers=search_headers, params=search_params)
search_resp.status_code
tweet_data = search_resp.json()
# ... tweet_data

for x in tweet_data['statuses']:
    print(x['text'] + '\n')


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