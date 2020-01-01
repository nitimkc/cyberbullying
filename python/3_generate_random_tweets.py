import glob 
from pathlib import Path
import pandas as pd
import os

# create random tweets to send for label
# make sure to not select a tweet already selected in previous random tweet file


PATH = r'/Users/peaceforlives/Documents/Projects/cyberbullying/data'
PATH_data = Path(PATH)                 # use your path

n = 5

# import previously selected random tweets 
in_files = glob.glob(os.path.join(PATH_data, 'random', "*.csv"))
insample = ( pd.read_csv(f) for f in in_files )

# combine all tweets from above to one object 
# select their id and set it as index

concat_insample = pd.concat(insample, ignore_index=True)
concat_insample['id'] = concat_insample['id'].astype(str)
concat_insample = concat_insample.set_index(concat_insample.id, inplace=False)
#concat_insample.head()
idx = concat_insample.index

# read and combine all files from send_for_label folder
# remove tweets with id matching index obtained above

all_files = glob.glob(os.path.join(PATH_data,'send_for_label', "*.csv"))  # advisable to use os.path.join as this makes concatenation OS independent
df_from_each_file = (pd.read_csv(f) for f in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=True)
concatenated_df['id'] = concatenated_df['id'].astype(str)
concatenated_df = concatenated_df[-concatenated_df.duplicated(['id'])]
concatenated_df.shape
nonsample_df = concatenated_df.loc[~concatenated_df['id'].isin(idx)]

# create new random sample from dataset that does not include previously samples tweets
# selected desired columns 
# export file to random folder

random_sample = nonsample_df.sample(n=1000)
cols= ['id', 'full_tweet', 'bullying_trace', 'bullying_role', 'form_of_bullying', 'bullying_post_type']
random_sample = random_sample[cols]
path_outfile = Path.joinpath(PATH_data, 'random',  ('random_tweets_'+ str(n) + '.csv') )
random_sample.to_csv(path_outfile, index=False, encoding = 'utf-8-sig')
