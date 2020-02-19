import glob 
from pathlib import Path
import pandas as pd
import os

PATH = r'/Users/peaceforlives/Documents/Projects/cyberbullying/data'
PATH_data = Path(PATH)

# import tweets with timezone info
path_infile = Path.joinpath(PATH_data, 'geotagged_tweets/geotagged_tweets.json')
data = pd.read_json(path_infile, lines=True)
data['localtime'] = pd.to_datetime(data['localtime'])
data.set_index('localtime', inplace=True)

# import matplotlib.pyplot as plt
# plt.plot(data['id'])
# plt.show()

# import tweets in random set     
# find localtime, timezone and state of those tweets based on their id            
in_files = glob.glob(os.path.join(PATH_data, 'random', "*.csv"))
insample = ( pd.read_csv(f) for f in in_files )
concat_insample = pd.concat(insample, ignore_index=True)
# concat_insample.set_index('id', inplace=True)

pd.merge(concat_insample, data, on='id', how='inner')

