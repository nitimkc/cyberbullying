# takes the original csv file sent for label
# takes the excel file returned with label
# adds the labels into the csv file
# exports the new csv file

# from pyexcel_xlsx import get_data
import time
import pandas as pd
import json
import os
from pathlib import Path

ROOT = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\'

JSON_CORPUS = Path(os.path.join(ROOT, 'data\\labelled_tweets'))
ORIGINAL_CORPUS = Path(os.path.join(ROOT, 'data\\send_for_label'))
LABELLED_B_CORPUS = Path(os.path.join(ROOT, 'data\\labelled_b'))

original_files = list(ORIGINAL_CORPUS.iterdir())
labelled_files = list(LABELLED_B_CORPUS.iterdir())

for i, j in zip(original_files,labelled_files):
    original = pd.read_csv(i, usecols=[0,1], index_col=None, encoding='utf-8-sig')
    labelled = pd.read_excel(j, index_col=None, encoding='utf-8-sig')

    original['bullying_trace'] = labelled['bullying_trace']
    original['bullying_role'] = labelled['bullying_role']
    original['form_of_bullying'] = labelled['form_of_bullying']
    original['bullying_post_type'] = labelled['bullying_post_type']
    
    data_json = original.to_dict(orient='records')
    # result = [json.dumps(record) for record in data_json]

    f_frmt = '.json'
    with open( Path(JSON_CORPUS, j.stem+f_frmt), 'w', encoding='utf-8-sig') as json_file:
        json_file.write(
            '\n'.join(json.dumps(record, ensure_ascii=False).encode('utf-8-sig', 'surrogatepass').decode('utf-8-sig') for record in data_json) +
            '\n'
        )