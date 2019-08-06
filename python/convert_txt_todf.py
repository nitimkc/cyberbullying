import pandas as pd
import json
from pandas.io.json import json_normalize

f = open("today.txt", "w+")
tweets = f.read()
#tweets = contents.replace("\n", "")
datajson = json.loads(tweets)
df = json_normalize(json.loads(datajson))
df.head(10)