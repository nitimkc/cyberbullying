import pymongo
import pandas as pd
from pymongo import MongoClient

client=MongoClient()
db=client.twitterdb
collection=db.twitter_search

data=pd.DataFrame(list(collection.find()))
print(data.tail(10))

df = data
df['full_tweet'] = df['extended_tweet'].apply(pd.Series)['full_text']
df.full_tweet.update(df.text)

match = ['mean',
 'force',
 'forced',
 'text',
 'texted',
 'online',
 'laugh',
 'laughing',
 'exclude',
 'excluded',
 'exclusion',
 'destroy',
 'destroyed',
 'force',
 'forced',
 'spread',
 'rumor',
 'rumour',
 'embarass',
 'embarassing',
 'embarassed',
 'repeatedly',
 'repeat',
 'mock',
 'mocked',
 'mocking',
 'tease',
 'teasing',
 'teased',
 'ignore',
 'ignored',
 'ignoring',
 'hitting',
 'hit',
 'gossip',
 'gossiped',
 'manipulate',
 'manipulating',
 'manipulated',
 'mislead',
 'misleading',
 'humiliating',
 'humiliated',
 'revenge',
 'insult',
 'insulted',
 'anonymous',
 'group text',
 'group chat',
 'isolate',
 'isolated',
 'social media',
 'rejection',
 'reject',
 'rejected',
 'aggressive',
 'intimidate',
 'intimidated',
 'jealous',
 'assault',
 'harass',
 'shove',
 'shoved',
 'pretend',
 'pretended',
 'scare',
 'scared',
 'shun',
 'shunned',
 'target',
 'targeted',
 'beat',
 'insult',
 'insulted',
 'threat',
 'threatened',
 'bash',
 'bashing',
 'degrade',
 'degrading',
 'perpetrated',
 'perpetrator',
 'defending',
 'stressful',
 'bystander',
 'coercion',
 'suicide',
 'facebook',
 'snapchat',
 'instagram',
 'whatsapp']

df['text'] = df['text'].str.lower()
df['extended_tweet'] = df['extended_tweet'].str.lower()
matched_idx = df['full_tweet'].str.contains('|'.join(match), case=False)
df_matched  = df[matched_idx]

#colnames = ['_id', 'created_at', 'id', 'text', 'truncated', 'geo', 'coordinates', 'place', 'lang', 'timestamp_ms', 'extended_tweet', 'extended_entities', 'possibly_sensitive', 'withheld_in_countries']
colnames = ['id', 'created_at', 'id', 'text', 'full_tweet', 'geo', 'coordinates', 'place', 'lang', 'timestamp_ms',]
df_matched = df_matched[colnames]


df_matched.to_csv(r'/Users/peaceforlives/Documents/Projects/cyberbullying/Data/Aug5.csv')