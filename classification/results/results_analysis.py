import os
import json
import pandas as pd
import matplotlib.pyplot as plt

gram = '1g2g'
FIG = '/TRACE'

ROOT = '/Users/peaceforlives/Documents/Projects/cyberbullying'
RESULTS = os.path.join(ROOT, 'results/', gram)
PLOTS = os.path.join(RESULTS, 'fig')

file = RESULTS+FIG+'_results.json'

df = pd.read_json(file, lines=True)
df.head()

new_df = pd.DataFrame(columns=df.columns[1:])
new_df['name'] = df.name

for i in df.columns[2:]:
    nes_ls = df[i].values.tolist()
    avg = [sum(ls)/len(ls) for ls in nes_ls]
    new_df[i] = pd.Series(avg)
new_df

sub_df = df.drop('model', axis=1) 
sub_df

df_lists = sub_df[['accuracy','precision','recall','f1','time']].unstack().apply(pd.Series)

score = 'f1'
plot_data = df_lists.T[score]
plot_data.columns = list(df.name)
plot_data.index = range(1,13)
plot_data

import pandas as pd
import numpy as np
# %matplotlib inline 
plt.rcParams['figure.figsize'] = [10, 5]
#f, ax = plt.subplots()
ax = plot_data.plot(style='.-')
plt.ylabel(score)
plt.xlabel('CV fold')
# plt.ylim(.40,1)
plt.title('{} score of each classifier over CV folds - {} model'.format(score, gram))
# plt.show()
plt.savefig(PLOTS+FIG+'_'+gram+'.png', bbox_inches='tight')