import pandas as pd
import json
#from pandas.io.json import json_normalize


with open('latest_tweets.txt') as f:
    data = json.load(f)
