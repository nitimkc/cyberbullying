
import os
from reader import TweetsCorpusReader
from timezonefinder import TimezoneFinder
import datetime as dt
import pytz
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

#windows
ROOT = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\'
CORPUS = os.path.join(ROOT, 'data\\original') #labelled_tweets\\ab')
RESULTS = os.path.join(ROOT, 'results')

#mac
# ROOT = '/Users/peaceforlives/Documents/Projects/cyberbullying/'
# CORPUS = os.path.join(ROOT, 'data/labelled_tweets')
# RESULTS = os.path.join(ROOT, 'results')

DOC_PATTERN = r'.*\.json' 

if __name__ == '__main__':
    corpus = TweetsCorpusReader(CORPUS, DOC_PATTERN) #, bullying_trace='coordinates')  # geo: lat, lon, coordinates: lon, lat
    docs = corpus.docs()

# from geopy.geocoders import Nominatim
# from geopy.exc import GeocoderTimedOut

# locator = Nominatim(user_agent='myGeocoder', timeout=0.85)

# for tweet in docs:
# # tweet = [t for t in docs if t['id_str']=='1169763041820512257'][0]
#     if tweet['coordinates']:
#         coordinates = str(tweet['coordinates']['coordinates'][::-1])[1:-1]
#         try:
#             address = locator.reverse(coordinates).raw['address']
#         except GeocoderTimedOut as e:
#             print("timeout error")
#             continue

#         if address['country_code'] in ['ca', 'us']:
#             print(address)
#             # if 'county' in address:
#             #     print(address)
#             #     tweet['location'] = (address['county'], address['state'])
#             # if 'city' in address:
#             #     print(address)                
#             #     tweet['location'] = (address['city'], address['state'])

# for tweet in docs:
#     if tweet['coordinates']!=None:
#         print(tweet['id'])

# import datetime as dt
# import pytz

# date = dt.datetime.strptime(docs[0]['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
# time = date.replace(tzinfo = pytz.timezone('UTC'))
# time.astimezone(pytz.timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S %Z%z')


# from timezonefinder import TimezoneFinder

# tf = TimezoneFinder()
# latitude, longitude = 2.75291954, 101.70681293
# tf.timezone_at(lng=longitude, lat=latitude) # returns 'Europe/Berlin'


locator = Nominatim(user_agent='myGeocoder', timeout=300)
tf = TimezoneFinder()

for tweet in docs:
# tweet = [t for t in docs if t['id_str']=='1169763041820512257'][0]
    if tweet['coordinates']:
        lat, lon = tweet['coordinates']['coordinates'][::-1]                  # get coordinates
        try:
            address = locator.reverse( str(lat)+' '+str(lon)).raw['address']  # get address from lookup
        except GeocoderTimedOut as e:
            print("timeout error")
            continue
        
        if address['country_code'] in ['ca', 'us']:                           # US or Canada
            tweet['tzone'] = tf.timezone_at(lng=lon, lat=lat)                 # convert to time format
            date = dt.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
            date = date.replace(tzinfo = pytz.timezone('UTC'))
            tweet['zone_dt'] = date.astimezone(pytz.timezone(tweet['tzone'])).strftime('%Y-%m-%d %H:%M:%S %Z%z')    # get time of local zone
            tweet['state'] = address['state']                                                                       # get the state/province 
            print(tweet['tzone'], tweet['zone_dt'], tweet['state'])
    else:
        tweet['tzone'], tweet['zone_dt'], tweet['state'] = [None]*3
