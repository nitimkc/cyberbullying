import os
import json
import pandas as pd
from pathlib import Path
from geo_analysis import get_timezone

PATH = '/Users/peaceforlives/Documents/Projects/cyberbullying/data/'
input_dir = 'filtered'     # data in folder
output_dir = 'located_tweets'   # data out folder

# files already process should not be processed
files_to_process = list( set( os.listdir(PATH+input_dir) ) - set( os.listdir(PATH+output_dir) ) )
# files_to_process = files_to_process[:20]
# file = 'tweets_2019-11-04.json'

for file in files_to_process:
    
    PATH_data = Path(PATH+input_dir)                     # go to input directory
    path_filename = PATH_data.joinpath(PATH_data, file)  # join filename to input directory
    print(path_filename)                                 # print full path of the file being processed
    
    data = []
    with open(path_filename) as f:
        for line in f:
            data.append(json.loads(line))
    
    path_outfile = Path.joinpath(PATH_data.parents[0], output_dir, path_filename.name)
    for tweet in data:
        new_tweet = get_timezone(tweet)
        with open(path_outfile, 'a') as f:
            f.write(json.dumps(new_tweet) + "\n")
