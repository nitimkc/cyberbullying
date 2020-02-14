import filtered_tweets as ft
import sendforlabel_tweets as sflt
from pathlib import Path
import os
import json
import pandas as pd

# take the data in original folder and 
# apply filtered_tweets function to the files in folder
# remove primary, secondary and additional keywords
# dump in filtered folder

primary = '/Users/peaceforlives/Documents/Projects/cyberbullying/python/primary_keywords.txt' 
secondary = '/Users/peaceforlives/Documents/Projects/cyberbullying/python/secondary_keywords.txt' 
additional = '/Users/peaceforlives/Documents/Projects/cyberbullying/python/additional_keywords.txt' 

PATH = '/Users/peaceforlives/Documents/Projects/cyberbullying/data/'
input_dir = 'original'    # data in folder
output_dir = 'filtered'   # data out folder

# files already process should not be processed
files_to_process = list( set( os.listdir(PATH+input_dir) ) - set( os.listdir(PATH+output_dir) ) )
# files_to_process = os.listdir(PATH+input_dir)

#path_infile = PATH + 'original/tweets_2019-09-01.json'

for file in files_to_process:
    PATH_data = Path(PATH+input_dir)                     # go to input directory
    path_filename = PATH_data.joinpath(PATH_data, file)  # join filename to input directory
    print(path_filename)                                 # print full path of the file being processed
    if '.DS_Store' in file:
        pass
    else:
        # apply filtered_tweets function to the file
        ft.filtered_tweets(path_infile=path_filename, primary=primary, secondary=secondary, additional=additional, output_dir=output_dir)


# load data from filtered folder 
# apply sendforlabel_tweets function to the files
# count urls, count hashtags and remove tweets with more than 5 hashtags, add columns for label
# dump it in send_for_label folder

input_dir = 'filtered'
output_dir = 'send_for_label'
    
for file in files_to_process:
    PATH_data = Path(PATH+input_dir)                     # go to input directory
    path_filename = PATH_data.joinpath(PATH_data, file)  # join filename to input directory
    print(path_filename)                                 # print full path of the file being processed
    if '.DS_Store' in file:
        pass
    else:
        # apply sendforlabel_tweets function to the file
        sflt.sendforlabel_tweets(path_infile=path_filename, output_dir=output_dir) 