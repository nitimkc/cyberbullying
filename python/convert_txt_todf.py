import pandas as pd
import json
from pandas.io.json import json_normalize


with open('latest_tweets.txt', 'r') as f:
    data = json.load(f, encoding="utf-8")
