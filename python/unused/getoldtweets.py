import GetOldTweets3 as got 

tweetCriteria = got.manager.TweetCriteria().setSince("2015-09-10")\
                                           .setUntil("2015-09-11")\
                                           .setMaxTweets(1)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
print(tweet.text)