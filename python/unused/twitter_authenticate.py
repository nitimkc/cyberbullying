
import tweepy
import app_credentials

import sys
import jsonpickle
import os

auth = tweepy.AppAuthHandler(app_credentials.consumerkey, app_credentials.consumersecret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)



searchQuery = 'bully OR bullied OR bullying'
maxTweets = 500 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
fName = 'tweets.txt' # We'll store the tweets in a text file.


# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = '2018-09-01'

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, tweet_mode='extended', lang = 'en', 
                    	since= '2019-06-01', until='2019-06-30', count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=searchQuery, tweet_mode='extended', lang = 'en',
                    	since= '2019-06-01', until='2019-06-30', count=tweetsPerQry, 
                    	since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, tweet_mode='extended', lang = 'en', 
                    	since= '2019-06-01', until='2019-06-30', count=tweetsPerQry,
                    	max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery,  tweet_mode='extended', lang = 'en', 
                    	since= '2019-06-01', until='2019-06-30', count=tweetsPerQry,
                    	max_id=str(max_id - 1), 
                    	since_id=sinceId)

            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                        '\n')
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
