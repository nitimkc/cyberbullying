import pandas as pd
import json
import os
from pathlib import Path
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import confusion_matrix

ROOT = '/Users/peaceforlives/Documents/Projects/cyberbullying/'
# ROOT = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\'

INTERRATER = Path(os.path.join(ROOT, 'interrater'))
SEND_FOR_LABEL = Path(os.path.join(INTERRATER, 'random'))
LABELLED_A_CORPUS = Path(os.path.join(INTERRATER, 'a'))
LABELLED_B_CORPUS = Path(os.path.join(INTERRATER, 'b'))

labelled_a_files = list(LABELLED_A_CORPUS.iterdir())
files = [i for i in labelled_a_files]
# files = [ files[2] ]

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
merged_df.set_index('id', inplace=True)
merged_df['bullying_trace_b'] = full_b['bullying_trace'].values
merged_df['bullying_role_b'] = full_b['bullying_role'].values
merged_df['form_of_bullying_b'] = full_b['form_of_bullying'].values
merged_df['bullying_post_type_b'] = full_b['bullying_post_type'].values
merged_df['full_tweet'] = [i.encode('utf-16','replace').decode('utf-16') for i in merged_df.full_tweet]
# merged_df.to_excel(r'merged_df.xlsx', index = False, encoding = 'utf16')


###################
label = 'bullying_trace'
###################
# cohen_kappa_score(merged_df[label], merged_df[label+'_b'])

test = merged_df[[label+'_b', label]].copy()
test = test.apply(lambda x: x.str.strip())

test = test[~test[label].str.contains("remove|nan")]
test = test[~test[label+'_b'].str.contains("remove|nan")]
# test['bullying_trace_b'] = ['no' if i=='remove' else i  for i in test['bullying_trace_b']]
# test['bullying_trace'] = ['no' if i=='remove' else i  for i in test['bullying_trace']]
cohen_kappa_score(test.bullying_trace, test.bullying_trace_b)
test[label].value_counts()
test[label+'_b'].value_counts()
confusion_matrix(test[label+'_b'], test[label])


###################
label = 'bullying_role'
###################
cohen_kappa_score(merged_df[label], merged_df[label+'_b'])

test = merged_df[[label+'_b', label]].copy()
test = test.apply( lambda x: x.str.strip() )

vals_to_replace = {'bystander':'other', 'reinforcer':'other', 'assistant':'other'}
test[label] = test[label].replace(vals_to_replace)
test[label+'_b'] = test[label+'_b'].replace(vals_to_replace)

test = test[~test[label].str.contains("nan")]
test = test[~test[label+'_b'].str.contains("nan")]
cohen_kappa_score(test[label], test[label+'_b'])
# test[label].value_counts()
# test[label+'_b'].value_counts()
# confusion_matrix(test[label+'_b'], test[label])


###########################
label = 'form_of_bullying'
###########################
cohen_kappa_score(merged_df[label], merged_df[label+'_b'])

test = merged_df[[label+'_b', label]].copy()
test = test.apply( lambda x: x.str.strip() )

test = test[~test[label].str.contains("nan")]
test = test[~test[label+'_b'].str.contains("nan")]
cohen_kappa_score(test[label], test[label+'_b'])
# test[label].value_counts()
# test[label+'_b'].value_counts()
confusion_matrix(test[label+'_b'], test[label])


###########################
label = 'bullying_post_type'
###########################

test = merged_df[[label+'_b', label]].copy()
test = test.apply( lambda x: x.str.strip() )

vals_to_replace = {'self disclosure':'self-disclosure', 'self-disclosures':'self-disclosure', 'reports':'report',
                    'accusations':'accusation', 'denials':'denial'}
test[label] = test[label].replace(vals_to_replace)
test[label+'_b'] = test[label+'_b'].replace(vals_to_replace)
cohen_kappa_score(test[label], test[label+'_b'])

test = test[~test[label].str.contains("nan")]
test = test[~test[label+'_b'].str.contains("nan")]
cohen_kappa_score(test[label], test[label+'_b'])
test[label].value_counts()
test[label+'_b'].value_counts()
confusion_matrix(test[label+'_b'], test[label])

# from sklearn.metrics import confusion_matrix
# confusion_matrix(test[label+'_b'], test[label])
