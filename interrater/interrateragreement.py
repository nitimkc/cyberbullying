import pandas as pd
import json
import os
from pathlib import Path
from sklearn.metrics import cohen_kappa_score

# ROOT = '/Users/peaceforlives/Documents/Projects/cyberbullying/'
ROOT = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\'

INTERRATER = Path(os.path.join(ROOT, 'interrater'))
SEND_FOR_LABEL = Path(os.path.join(ROOT, 'data/random'))
LABELLED_A_CORPUS = Path(os.path.join(ROOT, 'data/labelled_a'))
LABELLED_B_CORPUS = Path(os.path.join(ROOT, 'data/labelled_b'))

labelled_a_files = list(LABELLED_A_CORPUS.iterdir())
files = [i for i in labelled_a_files]

full_a = pd.DataFrame()
for i in files:
    print(i)
    labl_a = pd.read_excel(Path(os.path.join(LABELLED_A_CORPUS, i.stem+'.xlsx')), usecols=[0,1,2,3,4,5], index_col=None, encoding='utf-8-sig')
    full_a = full_a.append(labl_a)
    print(full_a.shape)
full_a = full_a.apply(lambda x: x.astype(str).str.lower())

full_b = pd.DataFrame()
for i in files:
    labl_b = pd.read_excel(Path(os.path.join(LABELLED_B_CORPUS, i.stem+'.xlsx')), usecols=[0,2,3,4,5], index_col=None, encoding='utf-8-sig')
    full_b = full_b.append(labl_b)
    print(full_b.shape)
full_b = full_b.apply(lambda x: x.astype(str).str.lower())


merged_df = full_a.copy()
merged_df['bullying_trace_b'] = full_b['bullying_trace']
merged_df['bullying_role_b'] = full_b['bullying_role']
merged_df['form_of_bullying_b'] = full_b['form_of_bullying']
merged_df['bullying_post_type_b'] = full_b['bullying_post_type']
merged_df = merged_df.reset_index()
merged_df.drop('index', axis=1, inplace=True)

merged_df['full_tweet'] = [i.encode('utf-16','replace').decode('utf-16') for i in merged_df.full_tweet]
# merged_df.to_excel(r'merged_df.xlsx', index = False, encoding = 'utf16')

cohen_kappa_score(merged_df.bullying_trace, merged_df.bullying_trace_b)

# test = merged_df[(merged_df['bullying_trace']!='remove') & (merged_df['bullying_trace_b']!='remove')]
test = merged_df[['bullying_trace_b', 'bullying_trace']].copy()
test.dropna(axis = 0, inplace=True)
test['bullying_trace_b'] = ['no' if i=='remove' else i  for i in test['bullying_trace_b']]
test['bullying_trace_b'] = test['bullying_trace_b'].str.strip()

test['bullying_trace'] = ['no' if i=='remove' else i  for i in test['bullying_trace']]
test['bullying_trace'] = test['bullying_trace'].str.strip()

cohen_kappa_score(test.bullying_trace, test.bullying_trace_b)

from sklearn.metrics import confusion_matrix
confusion_matrix(test['bullying_trace_b'], test['bullying_trace'])

from sklearn.metrics import f1_score
x = [1 if i=='yes' else 0 for i in test['bullying_trace'] ]
y = [1 if i=='yes' else 0 for i in test['bullying_trace_b'] ]
f1_score(x, y)