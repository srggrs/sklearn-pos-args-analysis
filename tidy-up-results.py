import os
import pandas as pd

WORK_PATH = os.path.abspath(os.path.dirname(__file__))
RESULT_FILE = os.path.join(WORK_PATH, 'out', 'data-summary.csv')

df = pd.read_csv(RESULT_FILE)
df = df.sort_values(['repo', 'file','class'])

df.to_csv(RESULT_FILE.replace('summary','summary-clean'), index=False)

df_agg = df.drop(['repo', 'file'], axis=1).groupby('class').agg(['sum', 'mean', 'min', 'max'])
df_agg.to_csv(RESULT_FILE.replace('summary', 'aggregate'))
print('done')
